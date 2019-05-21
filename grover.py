import cirq


def set_io_qubits(qubit_count):
    input_qubits = [cirq.GridQubit(i, 0) for i in range(qubit_count)]
    output_qubit = cirq.GridQubit(qubit_count, 0)
    return (input_qubits, output_qubit)


def oracle_method(input_qubits, output_qubit, x_иits):
    yield (cirq.X(q) for (q, bit) in zip(input_qubits, x_иits) if not bit)
    yield (cirq.TOFFOLI(input_qubits[0], input_qubits[1], output_qubit))
    yield (cirq.X(q) for (q, bit) in zip(input_qubits, x_иits) if not bit)


def grover_circuit_method(input_qubits, output_qubit, oracle):
    circuit = cirq.Circuit()
    circuit.append([
        cirq.X(output_qubit),
        cirq.H(output_qubit),
        cirq.H.on_each(*input_qubits),
    ])
    circuit.append(oracle)

    circuit.append(cirq.H.on_each(*input_qubits))
    circuit.append(cirq.X.on_each(*input_qubits))
    circuit.append(cirq.H.on(input_qubits[1]))
    circuit.append(cirq.CNOT(input_qubits[0], input_qubits[1]))
    circuit.append(cirq.H.on(input_qubits[1]))
    circuit.append(cirq.X.on_each(*input_qubits))
    circuit.append(cirq.H.on_each(*input_qubits))
    circuit.append(cirq.measure(*input_qubits, key='result'))
    return circuit


def bitstring(bits):
    return ''.join(str(int(b)) for b in bits)


if __name__ == '__main__':
    qubitCount = int(input("Count of qubits = "))
    circuit_sample_count = int(input("Circuits count = "))
    (input_qubits, output_qubit) = set_io_qubits(qubitCount)

    bits = [int(input("bit = ")) for _ in range(qubitCount)]
    xBits = []
    for x in bits:
        if x > 0:
            xBits.append(1);
        else:
            xBits.append(0);
    print('Secret bit sequence: {}'.format(xBits))

    oracle = oracle_method(input_qubits, output_qubit, xBits)

    circuit = grover_circuit_method(input_qubits, output_qubit, oracle)
    print('Circuit result :  ')
    print(circuit)
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=circuit_sample_count)

    frequencies = result.histogram(key='result', fold_func=bitstring)
    print('Sampled results:  {}'.format(frequencies))

    most_common_bitstring = frequencies.most_common(1)[0][0]
    print('Most common bitstring: {}'.format(most_common_bitstring))
    print('Found a match: {}'.format(
        most_common_bitstring == bitstring(xBits)))
