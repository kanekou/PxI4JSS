# PxI4JSS

Is is automatically generating Ising models from Petri nets for [Job Shop Scheduling Problem(JSS)](https://en.wikipedia.org/wiki/Job-shop_scheduling).

By importing a JSS Petri Net model created by a proprietary tool ([CPN Tools](https://cpntools.org/)), the model is automatically converted to an Ising Model. After that, The solver(PyQUBO Simulated Annealier) calculates the solution.

<!-- job4_exp.pdf here -->

## Why did we create this tool?

Quantum annealing has attracted attention as a fast algorithm for solving combinatorial optimization problems.
In this method, the combinatorial optimization problem is formulated in terms of an energy function called the [Ising model](https://en.wikipedia.org/wiki/Ising_model), which is then minimized to obtain the optimal solution.
However, the formulation of the Ising model requires a high level of expertise.

Our objective is to develop a method that makes it easy for non-specialists to formulate the Ising Model formulation.
As a result, modeling is possible with domain knowledge only.

As an approach, we developed a tool that models using [Petri nets](https://en.wikipedia.org/wiki/Petri_net) and automatically generates Ising models from them.
Petri nets are effective bipartite graphs, the property that formulas can be generated from diagrams.
Therefore, modeling graphically with Petri nets makes it easy to formulate without formulating equations.

<!-- ## What is JSS?

JSS is an optimization problem that seeks a schedule that minimizes the cost of processing multiple jobs consisting of multiple tasks. -->

## Usage

Please see above figure.

1. Create Petri Net by CPN tools
2. Export Petrinet as xml file
3. Input xml file in this library

### Input xml Example

Simple example. In detail, notebook example here.

```python
import pxi4jss
import cpntools4py

# Read petrinet created by CPN Tools
xml_path = '../inputs/jss_template.xml'
xml_doc = cpntools4py.read_xml(xml_path)
cpn = cpntools4py.CPN(xml_doc)
# To snakes objects
snakes_net = cpntools4py.to_snakes(cpn)
# Generating ising model and solving it.
res = pxi4jss.main(snakes_net)

print(res['solution']['energy'])
# => 0
print(res['solution']['end_time'])
# => 18
print(res['topology']['jobs'])
# =>
# {0: ['t0', 't1', 't2', 't3'],
#  1: ['t4', 't5', 't6', 't7'],
#  2: ['t8', 't9', 't10', 't11']}
```

## How JSS is represented in Petri Net by CPN Tools

By drawing the figure below, we can extract the problem structure from the Petri net.

E.g.) Jobs = 4, Each Task = 4, Resources = 3

<!-- jss_job4.pdf here-->

### Petri Net and JSS Mapping

- Transitions: Task

  - Fires when a machine processes a task and stops firing when it finishes.

- Place: Representation of system state and required resources.

  - It is divided into `task place` and `resource place`.

- Task place: with a plain token

  - Place token: Job processing status

- Resource place: with a resource place token

  - Resource place token: Machine actually used

<!-- TODO -->

## API references

## License

The source code is licensed MIT.
