# PxI4JSS

PxI4JSS automatically generates Ising models from Petri net models for [Job Shop Scheduling (JSS)](https://en.wikipedia.org/wiki/Job-shop_scheduling) Problem.

## Overview

By importing a Petri net model for JSS (Single Resource Type) created by [CPN Tools](https://cpntools.org/), our software generates an Ising (QUBO) model for the JSS problem.
After that, annealers for Ising (QUBO) models(e.g., [PyQUBO Simulated Annealier](https://pyqubo.readthedocs.io/en/latest/)) obtains solutions.

![job4_exp](/images/job4_exp.jpg)

## Why did we create this tool?

Quantum annealing has attracted attention as a new algorithm for solving combinatorial optimization problems. To use this method, we need to formulate the target combinatorial optimization problem as energy functions called the [Ising (QUBO) model](https://en.wikipedia.org/wiki/Ising_model).

However, the formulation of the Ising model requires expertise and skills.

Our objective is to develop a method that makes it easy for non-specialists to formulate Ising (QUBO) Models for their target problems with domain knowledge only.

As an approach, we developed a method that first models the target problem with [Petri nets](https://en.wikipedia.org/wiki/Petri_net) and generates Ising (QUBO) models from them.

Petri nets are a graphical modeling language. Therefore, we can graphically model our target optimization problems with Petri nets without formulating equations.

## Getting Started

Installing

```zsh
% pip install pxi4jss
```

## Usage

Please see above figure.

1. Create Petri nets by CPN tools
2. Export Petrinet as xml file
3. Input xml file and generate Petri net objects by [cpntools4py](https://pypi.org/project/cpntools4py/)
4. Generate and solve Ising models from Petri net objects by This package

### Example

Example from reading XML to solving Ising model. In detail, [notebook example here](https://github.com/kanekou/PxI4JSS/blob/main/example/example.ipynb).

```python
import pxi4jss
import cpntools4py

# Read petrinet created by CPN Tools
xml_path = './inputs/jss_job4.xml'
xml_doc = cpntools4py.read_xml(xml_path)
cpn = cpntools4py.CPN(xml_doc)
# To snakes objects
snakes_net = cpntools4py.to_snakes(cpn)
# Generating ising model and solving it
res = pxi4jss.main(snakes_net)

# Solution
print(res['solution']['energy'])
# => 0.0
print(res['solution']['end_time'])
# => 23
print(res['topology']['jobs']) # key: job, value: task
# =>
# {0: ['t0', 't1', 't2', 't3'],
#  1: ['t4', 't5', 't6', 't7'],
#  2: ['t8', 't9', 't10', 't11']}
```

## Modeling a JSS instance by CPNTools

We can model JSS instances.
The following figure shows an example with four jobs, four tasks per job, and one resource(machine) per each resource type.

![jss_job4](/images/jss_job4.jpg)

### Petri nets and JSS Mapping

![jss_job4_colored](/images/jss_job4_colored.jpg)

- Transitions: Task

  - Fires when a machine processes a task and stops firing when it finishes.
  - The firing time is set for each task as `processing time`.

- Place: Representation of system state and required resources.

  - It is divided into `task place` and `resource place`.

- Task place: with a place token

  - Place token: Job processing status

    **No need to configure in this package.**

- Resource place: with a resource place token

  - Resource place token: Machine actually used

## Prerequisites

- Python :: 3.x

  We have already confirmed the operation of version `3.7`.
  Other versions are also expected to work, but we have not been able to confirm.

## Versioning

We use pypi for versioning. For the versions available, see the tags on this repository.

## Running the tests

```python
% python3 -m unittest
```

## References

- https://pyqubo.readthedocs.io/en/latest/
- https://github.com/fpom/snakes
- https://pypi.org/project/cpntools4py/

## Contributing

Welcome!

## License

The source code is licensed MIT.
