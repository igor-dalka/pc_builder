def is_mobo_and_chassis_comp(motherboard, chassis):

    if not motherboard or not chassis:
        return None

    compatibility_map = {
        'ATX': ['ATX', 'Micro-ATX'],
        'Micro-ATX': ['Micro-ATX'],
    }

    supported = compatibility_map.get(chassis.form_factor, [])
    return motherboard.form_factor in supported

def is_mobo_and_cpu_comp(motherboard, cpu):

    if not motherboard or not cpu:
        return None

    return motherboard.socket == cpu.socket

def is_mobo_and_cpu_oc_comp(motherboard, cpu):
    
    if not motherboard or not cpu:
        return None
    
    mobo_oc = motherboard.oc_possible
    cpu_oc = cpu.oc_possible

    if mobo_oc and cpu_oc:
        return "OC ready"
    elif mobo_oc and not cpu_oc:
        return "Mobo can OC, but CPU can't"
    elif not mobo_oc and cpu_oc:
        return "CPU can OC, but Mobo can't"
    else:
        return "OC impossible"

def get_vrm_compatibility_status(motherboard, cpu):

    if not motherboard or not cpu:
        return None

    mobo_vrm = motherboard.VRM_quality
    cpu_required_vrm = cpu.minimum_VRM_quality

    if mobo_vrm > cpu_required_vrm:
        return "Sekcja zasilania jest więcej niż wystarczająca"
    elif mobo_vrm == cpu_required_vrm:
        return "Sekcja zasilania jest wystarczająca"
    else:
        return "Sekcja zasilania jest niewystarczająca - możliwy throttling przy podkręcaniu"
    
def get_ram_pair_info(motherboard):

    if not motherboard or motherboard.ram_slots is None:
        return None

    if motherboard.ram_slots >= 4:
        return "You can buy 2 pairs of ram"
    elif motherboard.ram_slots >= 2:
        return "You can buy only 1 pair of ram"
    
def is_ram_ddr_compatible_with_motherboard(ram, motherboard):

    if not ram or not motherboard:
        return None

    return ram.ddr_type == motherboard.ram_ddr

def get_ram_speed_compatibility_status(ram, motherboard):

    if not ram or not motherboard:
        return None

    ram_speed = ram.speed
    max_speed = motherboard.ram_max_speed

    if ram_speed > max_speed:
        return "RAM nie osiągnie swojej maksymalnej prędkości przez limit mobo"
    elif ram_speed == max_speed:
        return "RAM działa z maksymalną prędkością i wykorzystuje też maksymalną prędkość mobo"
    else:
        return "RAM działa z maksymalną prędkością, ale płyta główna obsługuje szybsze moduły"
    
def get_ram_capacity_status(ram, motherboard):

    if not ram or not motherboard:
        return None
    
    max_pairs = motherboard.ram_slots // 2
    total_capacity = ram.double_stick_capacity * max_pairs

    if total_capacity > motherboard.ram_max_capacity:
        return "Łączna pojemność RAM przekracza maksymalne możliwości płyty głównej"
    elif total_capacity == motherboard.ram_max_capacity:
        return "Wykorzystujesz pełną obsługiwaną pojemność RAM"
    else:
        return "Płyta główna może w przyszłości pomieścić więcej RAM"
    
def get_gpu_pcie_compatibility(gpu, motherboard):
    if not gpu or not motherboard:
        return None
    
    if motherboard.PCIE_16x_slot_type >= gpu.PCIE_16x_slot_type:
        return "Pełna zgodność PCIe slot jest wystarczająco szybki"
    else:
        return "Slot PCIe 16x jest starszej generacji, karta nie będzie osiągać maksymalnej wydajności!"
    
def get_m2_slot_status(motherboard):

    if not motherboard:
        return None

    if motherboard.M2_slots >= 3:
        return "Możesz zainstalować do 3 dysków M.2 NVMe"
    elif motherboard.M2_slots == 2:
        return "Możesz zainstalować do 2 dysków M.2 NVMe"
    elif motherboard.M2_slots == 1:
        return "Płyta główna wspiera tylko 1 dysk M.2 NVMe"
    else:
        return "Ta płyta główna nie posiada slotów M.2"
    
