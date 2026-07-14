from typing import Optional

Program = list[int]

def read_program(filename: str) -> Program:
    with open(filename, 'r') as f:
        start_memory: Program = [int(s) for s in f.read().rstrip().split(',')]
    return start_memory

Operation = tuple[str, int]
# int is number of steps so parameters + 1
opcodes: dict[int, Operation] = {
    1: ("+", 4),
    2: ("*", 4),
    3: ("in", 2),
    4: ("out", 2),
    5: ("jump-if-true", 3),
    6: ("jump-if-false", 3),
    7: ("<", 4),
    8: ("=", 4),
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
            _, _, out_addr = parameters
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
        elif action in {"<", "="}:
            a = get_value(0)
            b = get_value(1)
            result: bool
            if action == "<":
                result = a < b
            elif action == "=":
                result = a == b
            memory[parameters[2]] = int(result)
        elif action.startswith("jump-if"):
            test = bool(get_value(0))
            if action == 'jump-if-false':
                test = not test
            if test:
                ip = get_value(1)
                # skip increment
                continue
        else:
            raise ValueError(f"unknown opcode at {ip=} {action=}")
        ip += step
    return memory, output_queue
