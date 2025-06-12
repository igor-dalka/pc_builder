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

def get_mobo_and_cpu_oc_comp(motherboard, cpu):
    
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
        return "Możesz kupić dwie pary ramu"
    elif motherboard.ram_slots >= 2:
        return "Możesz kupić tylko jedną parę ramu"
    
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
    
def get_sata_disk_limit_info(motherboard, chassis):

    if not motherboard or not chassis:
        return None
    
    sata_ports = motherboard.SATA_slots
    disc_slots = chassis.all_disc_slots

    if sata_ports < disc_slots:
        return "Dostępne miejsca limituje liczba portów SATA na płycie głównej"
    elif disc_slots < sata_ports:
        return "Dostępne miejsca limituje liczba miejsc na dyski w obudowie"
    else:
        return "Obudowa i płyta mają taką samą maksymalną liczbę obsługiwanych dysków"
    
def get_max_fans_and_cpu_cooler_fans(motherboard, chassis, cpu_cooler):

    if not motherboard or not chassis or not cpu_cooler:
        return None
    
    fan_headers = motherboard.FAN_slots
    chassis_fan_slots = chassis.all_fan_slots
    cpu_cooler_fan_headers_needed = cpu_cooler.fan_headers_needed
    cpu_cooler_chassis_fan_slots_needed = cpu_cooler.chassis_fan_slots_needed
    max_fans = min((fan_headers - cpu_cooler_fan_headers_needed), (chassis_fan_slots - cpu_cooler_chassis_fan_slots_needed))

    if max_fans < 0:
        return "W zestawie brakuje miejsc do podłączenia wentylatorów w obudowie lub miejsc na wentylatory w obudowie!"
    
def is_AIO_possible(motherboard, cpu_cooler):

    if not motherboard or not cpu_cooler:
        return None
    
    mobo_waterpump_slot = motherboard.WATERPUMP_slot
    type_of_cooler = cpu_cooler.type_of_cooler

    if type_of_cooler == "AIO" and not mobo_waterpump_slot:
        return "Płyta główna nie obsługuje chłodzenia wodnego (brak gniazda waterpump)"
    elif type_of_cooler == "AIO":
        return "Chłodzenie wodne jest wspierane przez płytę główną"

def is_AIO_size_okay(cpu_cooler, chassis):
    
    if not chassis or not cpu_cooler:
        return None
    
    max_AIO_size = chassis.max_AIO_size
    AIO_size = cpu_cooler.AIO_size

    if max_AIO_size == AIO_size:
        return "Chłodzenie wodne idealnie pasuje do obudowy!"
    
    elif max_AIO_size > AIO_size:
        return "Chłodzenie wodne pasuje do obudowy, ale weszłoby większe"
    
    elif max_AIO_size < AIO_size:
        return "Chłodzenie nie wejdzie do obudowy!"
    
def is_ram_and_cpu_comp(processor, ram):
    
    if not processor or not ram:
        return None
    
    ram_type = ram.ddr_type
    processor_ram_type_ddr4 = processor.ddr4_compatible
    processor_ram_type_ddr5 = processor.ddr5_compatible

    if ram_type == 4 and processor_ram_type_ddr4:
        return "Ram ddr4 pasuje do tego procesora"
    elif ram_type == 5 and processor_ram_type_ddr5:
        return "Ram ddr5 pasuje do tego procesora"
    
def get_chassis_and_cpu_cooler_size_comp(chassis, cpu_cooler):

    if not chassis or not cpu_cooler:
        return None

    chassis_max_cpu_cooler_height = chassis.max_cpu_cooler_size
    cpu_cooler_height = cpu_cooler.height
    
    clearance = chassis.max_cpu_cooler_size - cpu_cooler.height

    if clearance < 0:
        return "To chłodzenie nie wejdzie do tej obudowy"
    elif clearance <= 5:
        return "To chłodzenie wejdzie na styk"
    else:
        return "To chłodzenie będzie pasować do tej obudowy z zapasem"
    
def get_mobo_and_cpu_cooler_comp(motherboard, cpu_cooler):

    if not motherboard or not cpu_cooler:
        return None
    
    mobo_socket = motherboard.socket
    cpu_cooler_sockets = cpu_cooler.sockets
    
    if mobo_socket in cpu_cooler_sockets:
        return "Chłodzenie pasuje do procesora"
    else:
        return "Chłodzenie nie pasuje do procesora"