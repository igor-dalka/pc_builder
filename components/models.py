from django.db import models

class Motherboard(models.Model):
    name = models.CharField(max_length=100)
    form_factor = models.CharField(max_length=50, null=True, blank=True)
    socket = models.CharField(max_length=50, null=True, blank=True)
    chipset = models.CharField(max_length=50, null=True, blank=True)
    ram_slots = models.IntegerField(null=True, blank=True)
    ram_ddr = models.IntegerField(null=True, blank=True)
    ram_max_speed = models.IntegerField(null=True, blank=True)
    ram_max_capacity = models.IntegerField(null=True, blank=True)
    audio_chipset = models.CharField(max_length=50, null=True, blank=True)
    ethernet_max_speed = models.IntegerField(null=True, blank=True)
    PCIE_16x_slots = models.IntegerField(null=True, blank=True)
    PCIE_16x_slot_type = models.FloatField(null=True, blank=True)
    PCIE_8x_slots = models.IntegerField(null=True, blank=True)
    PCIE_1x_slots = models.IntegerField(null=True, blank=True)
    M2_slots = models.IntegerField(null=True, blank=True)
    SATA_slots = models.IntegerField(null=True, blank=True)
    FAN_slots = models.IntegerField(null=True, blank=True)
    WATERPUMP_slot = models.BooleanField(null=True, blank=True)
    VRM_quality = models.IntegerField(null=True, blank=True)
    details = models.TextField(blank=True, null=True)
    fan_headers = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name

class Processor(models.Model):
    name = models.CharField(max_length=100)
    socket = models.CharField(max_length=50, null=True, blank=True)
    cores = models.IntegerField(null=True, blank=True)
    performance_cores = models.IntegerField(null=True, blank=True)
    efficient_cores = models.IntegerField(null=True, blank=True)
    threads = models.IntegerField(null=True, blank=True)
    single_core_speed = models.FloatField(null=True, blank=True)
    all_core_speed = models.FloatField(null=True, blank=True)
    real_all_core_speed = models.FloatField(null=True, blank=True)
    tdp = models.IntegerField(null=True, blank=True)
    igpu = models.BooleanField(null=True, blank=True)
    oc = models.BooleanField(null=True, blank=True)
    L3cache = models.IntegerField(null=True, blank=True)
    ddr4_compatible = models.IntegerField(null=True, blank=True)
    ddr5_compatible = models.IntegerField(null=True, blank=True)
    score = models.IntegerField(null=True, blank=True)
    oc_score = models.IntegerField(null=True, blank=True)
    minimum_VRM_quality = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name

class GraphicsCard(models.Model):
    name = models.CharField(max_length=100)
    VRAM = models.IntegerField(null=True, blank=True)
    PCIE_16x_slot_type = models.CharField(max_length=50, null=True, blank=True)
    tdp = models.IntegerField(null=True, blank=True)
    score = models.IntegerField(null=True, blank=True)
    
    def __str__(self):
        return self.name

class RAM(models.Model):
    name = models.CharField(max_length=100)
    single_stick_capacity = models.IntegerField(null=True, blank=True)
    double_stick_capacity = models.IntegerField(null=True, blank=True)
    ddr_type = models.IntegerField(null=True, blank=True)
    speed = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name

class PSU(models.Model):
    name = models.CharField(max_length=100)
    power = models.IntegerField(null=True, blank=True)
    cert = models.CharField(max_length=100, null=True, blank=True)
    details = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Chassis(models.Model):
    name = models.CharField(max_length=100)
    form_factor = models.CharField(max_length=50, null=True, blank=True)
    type = models.CharField(max_length=50, null=True, blank=True)
    glass_panel = models.BooleanField(null=True, blank=True)
    max_gpu_size = models.IntegerField(null=True, blank=True)
    max_cpu_cooler_size = models.IntegerField(null=True, blank=True)
    slot_2_5_inch = models.IntegerField(null=True, blank=True)
    slot_3_5_inch = models.IntegerField(null=True, blank=True)
    fan_slot_1 = models.CharField(max_length=50, null=True, blank=True)
    fan_slot_2 = models.CharField(max_length=50, null=True, blank=True)
    fan_slot_3 = models.CharField(max_length=50, null=True, blank=True)
    fan_slot_4 = models.CharField(max_length=50, null=True, blank=True)
    fan_slot_5 = models.CharField(max_length=50, null=True, blank=True)
    fan_slot_6 = models.CharField(max_length=50, null=True, blank=True)
    fan_slot_7 = models.CharField(max_length=50, null=True, blank=True)
    rgb_hub = models.BooleanField(null=True, blank=True)
    fan_hub = models.BooleanField(null=True, blank=True)
    PSU_placement = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name

class Fan(models.Model):
    name = models.CharField(max_length=100)
    size = models.IntegerField(null=True, blank=True)
    rgb = models.BooleanField(null=True, blank=True)
    CFM = models.FloatField(null=True, blank=True)
    decibels = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name

class Disc(models.Model):
    name = models.CharField(max_length=100)
    disc_type = models.CharField(max_length=50, null=True, blank=True)
    volume = models.IntegerField(null=True, blank=True)
    slot_type = models.CharField(max_length=50, null=True, blank=True)
    slot_size = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name

class CPU_cooler(models.Model):
    name = models.CharField(max_length=100)
    tdp = models.IntegerField(null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)
    can_add_fan = models.BooleanField(null=True, blank=True)
    decibels = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name


class Thermal_Paste(models.Model):
    name = models.CharField(max_length=100)
    conductivity = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name