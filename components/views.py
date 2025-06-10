from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Processor, Motherboard
from .compatibility import is_cpu_compatible_with_motherboard

class CpuMoboCompatibilityView(APIView):
    def get(self, request):
        try:
            cpu_id = request.GET.get('cpu_id')
            mobo_id = request.GET.get('motherboard_id')

            cpu = Processor.objects.get(id=cpu_id)
            mobo = Motherboard.objects.get(id=mobo_id)

            compatible = is_cpu_compatible_with_motherboard(cpu, mobo)

            response = {
                "cpu": cpu.name,
                "motherboard": mobo.name,
                "compatible": compatible,
            }

            if not compatible:
                response["message"] = f"Niekompatybilne sockety: CPU ({cpu.socket}) ≠ MOBO ({mobo.socket})"

            return Response(response, status=status.HTTP_200_OK)

        except (Processor.DoesNotExist, Motherboard.DoesNotExist, TypeError, ValueError):
            return Response({
                "compatible": None,
                "message": "Brakuje poprawnego ID CPU lub płyty głównej."
            }, status=status.HTTP_200_OK)