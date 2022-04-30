from pxi4jss.solver import main as solver
import snakes_utils

def main(snakes_net):
    # TODO: separate snakes_utils from here
    topology = snakes_utils.JSS(snakes_net, rflag='m')
    return solver(topology)



