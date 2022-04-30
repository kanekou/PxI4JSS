# PxI4JSS

Is is automatically generating Ising models from Petri nets for [Job Shop Scheduling Problem(JSS)](https://en.wikipedia.org/wiki/Job-shop_scheduling).

## Overview

By importing a JSS(Single Resource Type) Petri nets model created by a proprietary tool ([CPN Tools](https://cpntools.org/)), the model is automatically converted to an Ising Model. After that, The solver(PyQUBO Simulated Annealier) calculates the solution.

![job4_exp](/images/job4_exp.jpg)

## Why did we create this tool?

Quantum annealing has attracted attention as a fast algorithm for solving combinatorial optimization problems.
In this method, the combinatorial optimization problem is formulated in terms of an energy function called the [Ising model](https://en.wikipedia.org/wiki/Ising_model), which is then minimized to obtain the optimal solution.
However, the formulation of the Ising model requires a high level of expertise.

Our objective is to develop a method that makes it easy for non-specialists to formulate the Ising Model formulation.
As a result, modeling is possible with domain knowledge only.

As an approach, we developed a tool that models using [Petri nets](https://en.wikipedia.org/wiki/Petri_net) and automatically generates Ising models from them.
Petri nets are effective bipartite graphs, the property that formulas can be generated from diagrams.
Therefore, modeling graphically with Petri nets makes it easy to formulate without formulating equations.

## Getting Started

Installing

```zsh
% pip install pxi4jss
```

## Usage

Please see above figure.

1. Create Petri nets by CPN tools
2. Export Petrinet as xml file
3. Input xml file in this library

### Input xml Example

Simple example. In detail, [notebook example here](https://github.com/kanekou/PxI4JSS/blob/main/example/example.ipynb).

```python
import pxi4jss
import cpntools4py

# Read petrinet created by CPN Tools
xml_path = '../inputs/jss_job4.xml'
xml_doc = cpntools4py.read_xml(xml_path)
cpn = cpntools4py.CPN(xml_doc)
# To snakes objects
snakes_net = cpntools4py.to_snakes(cpn)
# Generating ising model and solving it.
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

## How JSS is represented in Petri nets by CPN Tools?

By drawing the figure below, this package can extract the problem structure from the Petri net.

E.g.) Jobs = 4, Each Task = 4, Resources = 3

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

## Contributing

Welcome!

## License

The source code is licensed MIT.
