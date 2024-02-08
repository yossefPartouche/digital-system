def extract_instruction(instruction):
    # Split the instruction by '=' to separate destination and the rest
    parts = instruction.split('=')
    
    # Extract the destination (if present)
    dest = parts[0].strip() if len(parts) > 1 else None
    
    # Split the rest by ';' to separate computation and jump (if present)
    if len(parts) > 1:
        comp_jump = parts[1].split(';')
        comp = comp_jump[0].strip()
        jump = comp_jump[1].strip() if len(comp_jump) > 1 else None
    else:
        comp = None
        jump = None
    
    return dest, comp, jump

    
