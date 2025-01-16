.. _api.devices:

``instrument.devices``
======================

See the advice below to declare your instrument's ophyd-style in YAML files:

* :ref:`api.configs.devices`
* :ref:`api.configs.devices_aps_only`

The `instrument.startup` module calls ``RE(make_devices())`` to
make the devices as described.

Declare all devices
-------------------

All ophyd-style devices are declared in one of the two YAML files listed above:

* when code (classes, factory functions) is provided by a package:
  * refer to the package class (or function) directly in the YAML file
* when local customization is needed (new support or modify a packaged class):
  * create local custom code that defines the class or factory
  * refer to local custom code in the YAML file

Any device can be created with python code that is compatible with
this API signature:

.. code-block:: py
    :linenos:

    callable(*, prefix="", name="", labels=[], **kwargs)

.. rubric:: Quick example

An ophyd object for an EPICS motor PV ``gp:m1`` is created in Python code where
``ophyd.EpicsMotor`` is the *callable*, ``"gp:m1"`` is the `prefix`, and the
other kwargs are ``name`` and ``labels``.

.. code-block:: py
    :linenos:

    import ophyd
    m1 = ophyd.EpicsMotor("ioc:m1", name="m1", labels=["motor"])

This YAML replaces all the Python code above to create the ``m1`` object:

.. code-block:: yaml
    :linenos:

    ophyd.EpicsMotor:
    - name: "m1"
      prefix: "ioc:m1"
      labels: ["motor"]

.. tip:: The devices are (re)created each time ``RE(make_devices())`` is run.

    If you edit either of these YAML files after starting your session, you can
    run ``RE(make_devices())`` again (without restarting your session) to
    (re)create the devices.  You only need to restart your session if you edit
    the Python code.

    The :func:`~instrument.utils.make_devices_yaml.make_devices()` plan stub
    imports the callable and creates any devices listed below it.  In YAML:

    * Each callable can only be listed once.
    * All devices that are created with a callable are listed below it.
    * Each device starts with a `-` and then the kwargs, as shown.

    Indentation is important. Follow the examples.

.. tip::  These YAML representations are functionally equivalent:

    See `yaml.org <https://yaml.org>`_ for more information and YAML examples.

    .. code-block:: yaml
        :linenos:

        ophyd.EpicsMotor:
        - name: m1
          prefix: ioc:m1
          labels:
            - motor

        ophyd.EpicsMotor:
        - {name: m1, prefix: ioc:m1, labels: ["motor"]}

        ophyd.EpicsMotor: [{name: m1, prefix: ioc:m1, labels: ["motor"]}]

Examples
--------

Examples are provided to show how to define your ophyd-style devices.

Packaged support
++++++++++++++++

Packaged support exists for many structures (motors, scalers,
area detectors, slits, shutters, ...).

Motors
~~~~~~

When support is used for more than one device, create a YAML list. Each item in
the list can be a dictionary with appropriate keyword arguments. This YAML code
describes five motors, using a one-line format for each dictionary.

.. code-block:: yaml
    :linenos:

    ophyd.EpicsMotor:
    - {name: m1, prefix: ioc:m1, labels: ["motor"]}
    - {name: m2, prefix: ioc:m2, labels: ["motor"]}
    - {name: m3, prefix: ioc:m3, labels: ["motor"]}
    - {name: dx, prefix: vme:m58:c0:m1, labels: ["motor"]}
    - {name: dy, prefix: vme:m58:c0:m2, labels: ["motor"]}

Scalers
~~~~~~~

This example creates a single scaler named `scaler`.  Two keyword
arguments are provided.

.. code-block:: yaml
    :linenos:

    ophyd.scaler.ScalerCH:
    - name: scaler
      prefix: ioc:scaler1
      labels: ["scalers", "detectors"]

Area detectors
~~~~~~~~~~~~~~

An area detector factory (from the ``apstools`` package) can be used to
declare one or more area detector devices.  Here's an instance of
ADSimDetector with various plugins.

.. code-block:: yaml
    :linenos:

    apstools.devices.ad_creator:
    - name: adsimdet
      prefix: "ad:"
      labels: ["area_detector", "detectors"]
      plugins:
      - cam:
            class: apstools.devices.SimDetectorCam_V34
      - image
      - pva
      - hdf1:
            class: apstools.devices.AD_EpicsFileNameHDF5Plugin
            read_path_template: "/mnt/iocad/tmp/"
            write_path_template: "/tmp/"
      - roi1
      - stats1

Local custom devices
++++++++++++++++++++

Sometimes, a package provides support that requires some local customization.

diffractometers
~~~~~~~~~~~~~~~

While the ``hklpy`` package provides a 6-circle diffractometer, it does
not provide a class with name substitutions for the motor axes.  We need those
substitutions to describe our diffractometer's motor assignments.
(That's a DIY feature for improvement in a future version of ``hklpy``.) We'll have
to make some local code that provides motor name substitutions as keyword
arguments.

Here's the local support code (in new file
``src/instrument/devices/diffractometers.py``):

.. code-block:: py
    :linenos:

    """Diffractometers"""

    import hkl
    from ophyd import Component
    from ophyd import EpicsMotor
    from ophyd import EpicsSignalRO
    from ophyd import FormattedComponent as FCpt

    class SixCircle(hkl.SimMixin, hkl.E6C):
        """
        Our 6-circle.  Eulerian.

        Energy obtained (RO) from monochromator.
        """

        # the reciprocal axes are defined by SimMixin

        mu = FCpt(EpicsMotor, "{prefix}{m_mu}", kind="hinted", labels=["motor"])
        omega = FCpt(EpicsMotor, "{prefix}{m_omega}", kind="hinted", labels=["motor"])
        chi = FCpt(EpicsMotor, "{prefix}{m_chi}", kind="hinted", labels=["motor"])
        phi = FCpt(EpicsMotor, "{prefix}{m_phi}", kind="hinted", labels=["motor"])
        gamma = FCpt(EpicsMotor, "{prefix}{m_gamma}", kind="hinted", labels=["motor"])
        delta = FCpt(EpicsMotor, "{prefix}{m_delta}", kind="hinted", labels=["motor"])

        energy = Component(EpicsSignalRO, "BraggERdbkAO", kind="hinted", labels=["energy"])
        energy_units = Component(EpicsSignalRO, "BraggERdbkAO.EGU", kind="config")

        def __init__(  # noqa D107
            self,
            prefix,
            *,
            m_mu="",
            m_omega="",
            m_chi="",
            m_phi="",
            m_gamma="",
            m_delta="",
            **kwargs,
        ):
            self.m_mu = m_mu
            self.m_omega = m_omega
            self.m_chi = m_chi
            self.m_phi = m_phi
            self.m_gamma = m_gamma
            self.m_delta = m_delta
            super().__init__(prefix, **kwargs)

The YAML description of our 6-circle diffractometer uses our local
custom ``SixCircle`` support with the assigned motors and other kwargs:

.. code-block:: yaml
    :linenos:

    instrument.devices.diffractometers.SixCircle:
    - name: sixc
      prefix: "gp:"
      labels: ["diffractometer"]
      m_mu: m23
      m_omega: m24
      m_chi: m25
      m_phi: m26
      m_gamma: m27
      m_delta: m28

Using the devices
-----------------

The :func:`instrument.utils.make_devices_yaml.make_devices()` plan stub adds all
devices to the command line level (the ``__main__`` namespace, as Python calls
it).  Plans or other code can obtain a reference to any of these devices through
use of the :data:`~instrument.utils.controls_setup.oregistry`.  The default
instrument provides a ``shutter`` device. This ``setup_shutter`` plan stub
configures the shutter to wait a finite time every time it opens or closes.

.. code-block:: py
    :linenos:

    def setup_shutter(delay=0.05):
        """
        Setup the shutter.

        Simulate a shutter that needs a finite recovery time after moving.
        """
        yield from bps.null()  # makes it a plan (generator function)

        shutter = oregistry["shutter"]
        shutter.wait_for_connection()
        shutter.delay_s = delay

With this YAML content:

.. code-block:: yaml
    :linenos:

    apstools.synApps.UserCalcsDevice: [{name: user_calcs, prefix: "gp:"}]

you might have a plan stub that needs two of the userCalcs.  The ``oregistry``
can provide them to your plan stub:

.. code-block:: py
    :linenos:

    dither_x = oregistry["user_calcs.calc9"]
    dither_y = oregistry["user_calcs.calc10"]
