"""
Make controls from YAML files
=============================

Construct ophyd-style devices from simple specifications in YAML files.

.. autosummary::

    ~Instrument
"""

__all__ = ["Instrument"]

import logging
import pathlib

import guarneri
from apstools.utils import dynamic_import

from ..utils.config_loaders import load_config_yaml

logger = logging.getLogger(__name__)
logger.bsdev(__file__)


class Instrument(guarneri.Instrument):
    """
    Custom YAML loader for guarneri.

    EXAMPLES:

    .. code-block:: yaml

        apstools.synApps.Optics2Slit2D_HV:
            - name: slit1
                prefix: ioc:Slit1
                labels: ["slits"]

        hkl.SimulatedE4CV:
            - name: sim4c
                prefix: ""
                labels: ["diffractometer"]

        ophyd.scaler.ScalerCH:
            - name: scaler1
                prefix: vme:scaler1
                labels: ["scalers", "detectors"]

        ophyd.EpicsMotor:
            - {name: m1, prefix: gp:m1, labels: ["motor"]}
            - {name: m2, prefix: gp:m2, labels: ["motor"]}
            - {name: m3, prefix: gp:m3, labels: ["motor"]}
            - {name: m4, prefix: gp:m4, labels: ["motor"]}
    """

    def parse_yaml_file(self, config_file: pathlib.Path | str) -> list[dict]:
        """Read device configurations from YAML format file."""
        if isinstance(config_file, str):
            config_file = pathlib.Path(config_file)

        def parse(class_name, specs):
            if class_name not in self.device_classes:
                self.device_classes[class_name] = dynamic_import(class_name)
            entries = []
            for table in specs:
                entry = {
                    "device_class": class_name,
                    "args": (),  # ALL specs are kwargs!
                    "kwargs": table,
                }
                entries.append(entry)
            return entries

        controls = load_config_yaml(config_file)
        devices = []
        for k, v in controls.items():
            devices += parse(k, v)
        return devices
