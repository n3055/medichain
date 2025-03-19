import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import ProductImage, RentalRequest, SubRentalRequest

# 🚀 Upload Product Image
@csrf_exempt
def upload_product_image(request):
    if request.method == "POST" and request.FILES.get("image"):
        pid = request.POST.get("pid")
        owner = request.POST.get("owner")
        image = request.FILES["image"]

        product_image, created = ProductImage.objects.update_or_create(
            pid=pid, defaults={"owner": owner, "image": image}
        )
        return JsonResponse({"message": "Image uploaded successfully", "pid": pid, "owner": owner})
    
    return JsonResponse({"error": "Invalid request"}, status=400)

# 🚀 Create Rental Request (User Requests a Product)
@csrf_exempt
def create_rental_request(request):
    if request.method == "POST":
        data = json.loads(request.body)
        rental, created = RentalRequest.objects.get_or_create(
            pid=data["pid"], owner=data["owner"], renter=data["renter"], status="Pending"
        )
        return JsonResponse({"message": "Rental request created", "pid": data["pid"], "owner": data["owner"], "renter": data["renter"], "status": rental.status})

# 🚀 Approve Rental Request (Owner Approves)
@csrf_exempt
def approve_rental_request(request):
    if request.method == "POST":
        data = json.loads(request.body)
        rental = RentalRequest.objects.filter(pid=data["pid"], owner=data["owner"], renter=data["renter"]).first()
        
        if rental:
            rental.status = "Approved"
            rental.save()
            return JsonResponse({"message": "Rental request approved", "pid": data["pid"], "status": "Approved", "owner": data["owner"], "renter": data["renter"]})
        
        return JsonResponse({"error": "Rental request not found"}, status=404)

# 🚀 Create Sub-Rental Request (Renter Requests Sub-Rent)
@csrf_exempt
def create_sub_rental_request(request):
    if request.method == "POST":
        data = json.loads(request.body)
        sub_rental, created = SubRentalRequest.objects.get_or_create(
            pid=data["pid"], owner=data["owner"], renter=data["renter"], sub_renter=data["sub_renter"], status="Pending"
        )
        return JsonResponse({"message": "Sub-rental request created", "pid": data["pid"], "owner": data["owner"], "renter": data["renter"], "sub_renter": data["sub_renter"], "status": sub_rental.status})

# 🚀 Approve Sub-Rental Request (Owner Approves)
@csrf_exempt
def approve_sub_rental_request(request):
    if request.method == "POST":
        data = json.loads(request.body)
        sub_rental = SubRentalRequest.objects.filter(pid=data["pid"], owner=data["owner"], renter=data["renter"], sub_renter=data["sub_renter"]).first()
        
        if sub_rental:
            sub_rental.status = "Approved"
            sub_rental.save()
            return JsonResponse({"message": "Sub-rental request approved", "pid": data["pid"], "status": "Approved", "owner": data["owner"], "renter": data["renter"], "sub_renter": data["sub_renter"]})
        
        return JsonResponse({"error": "Sub-rental request not found"}, status=404)

# 🚀 Get User Dashboard (Rented & Owned Products)
@csrf_exempt
def get_dashboard(request):
    if request.method == "GET":
        public_address = request.GET.get("address")
        
        owned_requests = RentalRequest.objects.filter(owner=public_address)
        rented_requests = RentalRequest.objects.filter(renter=public_address)
        sub_rented_requests = SubRentalRequest.objects.filter(sub_renter=public_address)

        return JsonResponse({
            "owned_products": list(owned_requests.values()),
            "rented_products": list(rented_requests.values()),
            "sub_rented_products": list(sub_rented_requests.values()),
        })

def home(request):
    return render(request,"home.html")

def dash(request):
    return render(request,"index.html")


