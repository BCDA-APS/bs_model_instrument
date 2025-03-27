APS Bluesky Software Ecosystem Overview
=======================================

This document provides an overview of key GitHub repositories maintained and used by the APS for integrating the `Bluesky` data acquisition framework into beamline operations.

BITS Ecosystem Diagram
----------------------

The following figure describes the relationships among the various repositories and modules that compose or support the BITS framework at APS.

.. graphviz::

   digraph BITS_Ecosystem {
       rankdir=LR;
       node [shape=box style=filled fillcolor=lightgrey fontname="Arial"];

       BITS [label="BITS\n(Main Package)", shape=ellipse, fillcolor=lightblue];
       BITS_Starter [label="BITS-Starter\n(Starter Repo)"];
       apsbits [label="apsbits\n(Core Functionality)"];
       demo_instr [label="demo_instrument\n(Standard Instrument)"];
       demo_qserver [label="demo_qserver\n(Standard QServer)"];
       apstools [label="apstools\n(Devices, Plans, Callbacks)", shape=ellipse, fillcolor=lightyellow];
       guarneri [label="guarneri\n(Ophyd Loader)", shape=ellipse, fillcolor=lightyellow];
       hkl2 [label="hkl2\n(Diffraction Tools)", shape=ellipse, fillcolor=lightyellow];
       training [label="Bluesky_training\n(Training Resources)", shape=ellipse, fillcolor=lightyellow];

       BITS -> BITS_Starter [label="template for"];
       BITS -> apsbits [label="includes"];
       apsbits -> demo_instr [label="provides"];
       apsbits -> demo_qserver [label="provides"];
       BITS -> apstools [label="uses"];
       BITS -> guarneri [label="uses"];
       BITS -> hkl2 [label="uses"];
       training -> BITS [label="supports"];
   }

Repository Descriptions
-----------------------

- **`BITS <https://github.com/BCDA-APS/BITS>`_**

  The central repository for APS efforts to integrate Bluesky into beamline environments. It provides configuration, utilities, and architectural support for deploying Bluesky-based instruments at the APS.

- **`BITS-Starter <https://github.com/BCDA-APS/BITS-Starter/>`_**

  A template repository for creating new BITS-compatible Bluesky instruments. Offers a boilerplate structure to streamline deployment.

- **`apsbits` (submodule in BITS)**

  Core BITS functionality. Encapsulates the logic and base configurations used by BITS instruments.

  - `apsbits/demo_instrument`: A reference Bluesky instrument showcasing a standard BITS-compliant setup.
  - `apsbits/demo_qserver`: A reference QServer that integrates with the demo instrument.

- **`apstools <https://github.com/BCDA-APS/apstools>`_**

  A general-purpose utility library with reusable Bluesky components:

  - `apstools.devices`: Collection of commonly used Ophyd devices across APS beamlines.
  - `apstools.plans`: Frequently used Bluesky plans tailored to APS experiments.
  - `apstools.callbacks`: Ready-made Bluesky callbacks for logging, visualization, and monitoring.

- **`guarneri <https://github.com/spc-group/guarneri>`_**

  A device registry and dynamic loader for Ophyd. Simplifies the instantiation and reuse of instrument configurations.

- **`hkl2`**

  Helper tools for crystallographic diffraction workflows. Supports integration with Bluesky and orientation matrix calculations.

- **`Bluesky_training`**

  A complete training suite developed to support APS beamline scientists and users adopting the Bluesky ecosystem. Includes examples, tutorials, and curriculum materials.

Summary
-------

These packages form a modular and extensible software stack supporting the transition to Bluesky at APS. They emphasize reuse, standardization, and training, enabling robust and scalable data acquisition workflows across beamlines.

