import numpy as np

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, execute
from qiskit.tools.visualization import plot_vectors


def main():
    q = QuantumRegister(1)
    c = ClassicalRegister(1)

    pre = QuantumCircuit(q, c)
    pre.h(q)
    pre.barrier()

    meas_x = QuantumCircuit(q, c)
    meas_x.barrier()
    meas_x.h(q)
    meas_x.measure(q, c)

    meas_y = QuantumCircuit(q, c)
    meas_y.barrier()
    meas_y.s(q).inverse()
    meas_y.h(q)
    meas_y.measure(q, c)

    meas_z = QuantumCircuit(q, c)
    meas_z.barrier()
    meas_z.measure(q, c)

    bloch_vector = ['x', 'y', 'z']
    exp_vector = range(0, 21)
    circuits = []
    for exp_index in exp_vector:
        middle = QuantumCircuit(q, c)
        phase = 2 * np.pi * exp_index / (len(exp_vector) - 1)
        middle.u1(phase, q)
        circuits.append(pre + middle + meas_x)
        circuits.append(pre + middle + meas_y)
        circuits.append(pre + middle + meas_z)

    job = execute(circuits, backend="local_qasm_simulator", shots=1024)
    result = job.result()

    for exp_index in exp_vector:
        bloch = [0, 0, 0]
        for bloch_index in range(len(bloch_vector)):
            data = result.get_counts(circuits[3 * exp_index + bloch_index])
            try:
                p0 = data["0"] / 1024.0
            except KeyError:
                p0 = 0
            try:
                p1 = data['1'] / 1024.0
            except KeyError:
                p1 = 0
            bloch[bloch_index] = p0 - p1
        plot_bloch_vector(bloch)


if __name__ == "__main__":
    main()
