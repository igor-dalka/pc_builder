from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from django.apps import apps

class ComponentListView(APIView):
    def get(self, request, component_type):
        try:
            model = apps.get_model('components', component_type.lower())
        except LookupError:
            return Response({"error": "Invalid component type"}, status=status.HTTP_400_BAD_REQUEST)

        components = model.objects.all()
        data = []

        for item in components:
            if component_type == "cpu":
                details = {
                    "socket": item.socket,
                    "cores": item.cores,
                    "threads": item.threads,
                    "tdp": item.tdp,
                    "OC": item.oc_possible,
                    "iGPU": item.igpu,
                    "score": item.score,
                    "VRM required": item.minimum_VRM_quality,
                }

            elif component_type == "motherboard":
                details = {
                    "socket": item.socket,
                    "form factor": item.form_factor,
                    "VRM quality": item.VRM_quality,
                    "OC": item.oc_possible,
                    "RAM slots": item.ram_slots,
                    "DDR": item.ram_ddr,
                    "Max RAM speed": item.ram_max_speed,
                    "M.2 slots": item.M2_slots,
                    "SATA ports": item.SATA_slots,
                    "FAN headers": item.FAN_slots,
                    "Waterpump header": item.WATERPUMP_slot,
                }

            elif component_type == "gpu":
                details = {
                    "VRAM (GB)": item.VRAM,
                    "PCIe version": item.PCIE_16x_slot_type,
                    "TDP": item.tdp,
                    "Score": item.score,
                }

            elif component_type == "ram":
                details = {
                    "DDR type": item.ddr_type,
                    "Speed (MHz)": item.speed,
                    "Single stick": item.single_stick_capacity,
                    "Double stick": item.double_stick_capacity,
                }

            elif component_type == "psu":
                details = {
                    "Power (W)": item.power,
                    "Certificate": item.cert,
                    "Extra info": item.details,
                }

            elif component_type == "chassis":
                details = {
                    "Form factor": item.form_factor,
                    "Glass panel": item.glass_panel,
                    "Max GPU size (mm)": item.max_gpu_size,
                    "Max CPU cooler (mm)": item.max_cpu_cooler_size,
                    "Max AIO size (mm)": item.max_AIO_size,
                    "Disc slots": item.all_disc_slots,
                    "Fan slots": item.all_fan_slots,
                    "RGB hub": item.rgb_hub,
                    "Fan hub": item.fan_hub,
                }

            elif component_type == "fan":
                details = {
                    "Size (mm)": item.size,
                    "RGB": item.rgb,
                    "Airflow (CFM)": item.CFM,
                    "Noise (dB)": item.decibels,
                }

            elif component_type == "disc":
                details = {
                    "Type": item.disc_type,
                    "Capacity (GB)": item.volume,
                    "Slot type": item.slot_type,
                }

            elif component_type == "cpu_cooler":
                details = {
                    "Cooler type": item.type_of_cooler,
                    "TDP": item.tdp,
                    "Height (mm)": item.height,
                    "Fan headers needed": item.fan_headers_needed,
                    "Chassis fan slots needed": item.chassis_fan_slots_needed,
                    "AIO size (mm)": item.AIO_size,
                    "Add extra fan": item.can_add_fan,
                    "Noise (dB)": item.decibels,
                }

            elif component_type == "thermal_paste":
                details = {
                    "Conductivity (W/mK)": item.conductivity,
                }

            else:
                details = {"info": str(item)}

            data.append({
                "id": item.id,
                "name": item.name,
                "details": details,
            })

        return Response(data)
    
class ComponentDetailView(APIView):
    def get(self, request, component_type, component_id):
        try:
            model = apps.get_model('components', component_type.lower())
        except LookupError:
            return Response({"error": "Invalid component type"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            item = model.objects.get(id=component_id)
        except model.DoesNotExist:
            return Response({"error": "Component not found"}, status=status.HTTP_404_NOT_FOUND)

        data = {
            field.name: getattr(item, field.name)
            for field in model._meta.fields
        }

        return Response(data)
    
class PCBuildDetailView(APIView):
    def get(self, request, build_id):
        try:
            build = PCBuild.objects.get(id=build_id)
        except PCBuild.DoesNotExist:
            return Response({"error": "Build not found"}, status=status.HTTP_404_NOT_FOUND)

        data = {
            "id": build.id,
            "name": build.name,
            "components": {
                "cpu": build.cpu.name if build.cpu else None,
                "motherboard": build.motherboard.name if build.motherboard else None,
                "gpu": build.gpu.name if build.gpu else None,
                "ram": build.ram.name if build.ram else None,
                "psu": build.psu.name if build.psu else None,
                "chassis": build.chassis.name if build.chassis else None,
                "cpu_cooler": build.cpu_cooler.name if build.cpu_cooler else None,
                "disc": build.disc.name if build.disc else None,
                "thermal_paste": build.thermal_paste.name if build.thermal_paste else None,
            }
        }

        return Response(data, status=status.HTTP_200_OK)