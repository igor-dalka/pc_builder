from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers
from .models import *
from django.apps import apps
from .compatibility import *
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.views import View
from django.shortcuts import render

class PCBuildUIView(View):
    def get(self, request):
        return render(request, "build_ui.html", {
            "cpus": cpu.objects.all(),
            "mobos": motherboard.objects.all(),
            "rams": ram.objects.all(),
            "gpus": gpu.objects.all(),
            "psus": psu.objects.all(),
            "chassis": chassis.objects.all(),
            "cpu_coolers": cpu_cooler.objects.all(),
            "discs": disc.objects.all(),
            "thermal_pastes": thermal_paste.objects.all(),
        })

    def post(self, request):
        def safe_get(model, id_value):
            try:
                return model.objects.get(id=int(id_value))
            except (ValueError, model.DoesNotExist, TypeError):
                return None

        cpu_id = request.POST.get("cpu")
        mobo_id = request.POST.get("motherboard")
        ram_id = request.POST.get("ram")
        gpu_id = request.POST.get("gpu")
        psu_id = request.POST.get("psu")
        chassis_id = request.POST.get("chassis")
        cooler_id = request.POST.get("cpu_cooler")
        disc_id = request.POST.get("disc")
        thermal_id = request.POST.get("thermal_paste")

        selected_cpu = safe_get(cpu, cpu_id)
        selected_mobo = safe_get(motherboard, mobo_id)
        selected_ram = safe_get(ram, ram_id)
        selected_gpu = safe_get(gpu, gpu_id)
        selected_psu = safe_get(psu, psu_id)
        selected_chassis = safe_get(chassis, chassis_id)
        selected_cooler = safe_get(cpu_cooler, cooler_id)
        selected_disc = safe_get(disc, disc_id)
        selected_thermal = safe_get(thermal_paste, thermal_id)

        alerts = []
        if selected_cpu and selected_mobo:
            if not is_mobo_and_cpu_comp(selected_mobo, selected_cpu):
                alerts.append("nie działa")

        return render(request, "_compatibility_alert.html", {"alerts": alerts})

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
    
from .models import PCBuild

class PCBuildSerializer(serializers.ModelSerializer):
    class Meta:
        model = PCBuild
        fields = '__all__'


class PCBuildCreateView(APIView):
    def post(self, request):
        serializer = PCBuildSerializer(data=request.data)
        if serializer.is_valid():
            build = serializer.save()
            return Response({
                "message": "Build zapisany!",
                "build_id": build.id,
                "url": f"/builds/{build.id}/"
            }, status=201)
        return Response(serializer.errors, status=400)
    
class CompatibilityCheckView(APIView):
    def post(self, request):
        data = request.data
        response = {}

        def get_component(model, key):
            _id = data.get(key)
            if _id:
                try:
                    return model.objects.get(id=_id)
                except model.DoesNotExist:
                    response[key] = {"error": f"{model.__name__} with ID {_id} not found"}
            return None

        selected_cpu = get_component(cpu, "cpu")
        selected_mobo = get_component(motherboard, "motherboard")
        selected_ram = get_component(ram, "ram")
        selected_gpu = get_component(gpu, "gpu")
        selected_chassis = get_component(chassis, "chassis")
        selected_cooler = get_component(cpu_cooler, "cpu_cooler")

        if selected_mobo and selected_chassis:
            response["mobo_and_chassis"] = is_mobo_and_chassis_comp(selected_mobo, selected_chassis)

        if selected_mobo and selected_cpu:
            response["mobo_and_cpu"] = is_mobo_and_cpu_comp(selected_mobo, selected_cpu)
            response["mobo_cpu_oc"] = get_mobo_and_cpu_oc_comp(selected_mobo, selected_cpu)
            response["vrm_compatibility"] = get_vrm_compatibility_status(selected_mobo, selected_cpu)

        if selected_mobo:
            response["ram_pair_info"] = get_ram_pair_info(selected_mobo)

        if selected_ram and selected_mobo:
            response["ram_ddr_compatible"] = is_ram_ddr_compatible_with_motherboard(selected_ram, selected_mobo)
            response["ram_speed_status"] = get_ram_speed_compatibility_status(selected_ram, selected_mobo)
            response["ram_capacity_status"] = get_ram_capacity_status(selected_ram, selected_mobo)

        if selected_gpu and selected_mobo:
            response["gpu_pcie_compatibility"] = get_gpu_pcie_compatibility(selected_gpu, selected_mobo)

        if selected_mobo:
            response["m2_slot_status"] = get_m2_slot_status(selected_mobo)

        if selected_mobo and selected_chassis:
            response["sata_disk_limit_info"] = get_sata_disk_limit_info(selected_mobo, selected_chassis)

        if selected_mobo and selected_chassis and selected_cooler:
            response["fan_and_cooler_fan_status"] = get_max_fans_and_cpu_cooler_fans(selected_mobo, selected_chassis, selected_cooler)

        if selected_mobo and selected_cooler:
            response["aio_possible"] = is_AIO_possible(selected_mobo, selected_cooler)

        if selected_cooler and selected_chassis:
            response["aio_size_fit"] = is_AIO_size_okay(selected_cooler, selected_chassis)

        if selected_ram and selected_cpu:
            response["ram_and_cpu_compatibility"] = is_ram_and_cpu_comp(selected_cpu, selected_ram)

        if selected_chassis and selected_cooler:
            response["chassis_and_cooler_fit"] = get_chassis_and_cpu_cooler_size_comp(selected_chassis, selected_cooler)

        if selected_mobo and selected_cooler:
            response["cooler_and_mobo_socket"] = get_mobo_and_cpu_cooler_comp(selected_mobo, selected_cooler)

        return Response(response, status=status.HTTP_200_OK)