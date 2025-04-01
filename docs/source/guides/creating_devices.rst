.. _creating_devices:

Adding Devices to an Instrument
----

Every new instrument comes pre-loaded with a simulated motor and a detector. To add a new device to your instrument startup a couple of steps must be taken. 

1. Create a new device class in the devices folder

.. code-block:: python

    from ophyd import Device, EpicsMotor
    from ophyd import Component as Cpt

    class StageXY(Device):
        x = Cpt(EpicsMotor, ':X')
        y = Cpt(EpicsMotor, ':Y')

2. Add the new device class to the device __init__ file

- If you want to use a device from an external package, make sure to add it to the __init__ file in the device folder of your instrument.

.. code-block:: python

    from .stage_xy import StageXY
    from apstools.synApps import Optics2Slit2D_HV

3. Add the new device to the instrument configuration file

.. code-block:: yaml

    instrument.devices.StageXY:
    - name: stage
      prefix: BITS
      labels: ["motors"]

     apstools.synApps.Optics2Slit2D_HV:
     - name: slit1
       prefix: ioc:Slit1
       labels: ["slits"]


.. tip::
    All kwargs of your device can be specified in the yaml file making it easy to resuse classes.

.. tip::
`APSTOOLS <https://github.com/BCDA-APS/apstools/tree/main/apstools>`_ has a lot of devices commonly used at the APS. Consider first checking the package and overwriting the device class to fit your needs before creating a new device.