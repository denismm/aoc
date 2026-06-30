from typing import Optional

Program = list[int]

def read_program(filename: str) -> Program:
    with open(filename, 'r') as f:
        start_memory: Program = [int(s) for s in f.read().rstrip().split(',')]
    return start_memory

Operation = tuple[str, int]
opcodes: dict[int, Operation] = {
    1: ("+", 4),
    2: ("*", 4),
    3: ("in", 2),
    4: ("out", 2),
    99: ("halt", 1),
}


def run_program(start_memory: Program, input_queue: Optional[list[int]] = None) -> tuple[Program, list[int]]:
    if input_queue is None:
        input_queue = []
    output_queue = []
    memory: Program = list(start_memory)
    ip = 0

    parameters: list[int] = []
    modes: list[str] = []

    def get_value(position: int) -> int:
        param = parameters[position]
        mode = modes[position]
        if mode == '1':
            return param
        elif mode == '0':
            return memory[param]
        else:
            raise ValueError(f"unknown mode {mode}")

    while True:
        raw_instruction: int = memory[ip]
        mode_int: int = raw_instruction // 100
        instruction: int = raw_instruction % 100
        operation: Operation = opcodes[instruction]
        (action, step) = operation
        modes = list(reversed(str(mode_int)))
        parameters = memory[ ip+1 : ip+step]
        if len(modes) < len(parameters):
            modes += ("0") * (len(parameters) - len(modes))
        if action == 'halt':
            break
        elif action in {"*", "+"}:
            a_addr, b_addr, out_addr = parameters
            a = get_value(0)
            b = get_value(1)
            if action == '+':
                out = a + b
            elif action == '*':
                out = a * b
            else:
                raise ValueError(f"unknown opcode at {ip=} {action=}")
            memory[out_addr] = out
        elif action == 'in':
            data = input_queue.pop()
            out_addr = parameters[0]
            memory[out_addr] = data
        elif action == 'out':
            output_queue.append(get_value(0))
        else:
            raise ValueError(f"unknown opcode at {ip=} {action=}")
        ip += step
    return memory, output_queue
