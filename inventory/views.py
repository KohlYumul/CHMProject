from django.shortcuts import render, get_object_or_404, redirect
from accounts.decorators import role_required
from .models import Medication, MedicalSupply, Equipment
from .forms import MedicationForm, MedicalSupplyForm, EquipmentForm
from django.contrib import messages
from hospitals.models import Hospital
from django.urls import reverse
from django.http import Http404


# =======================
# HELPER
# =======================
def get_user_hospital(request):
    """Return the hospital for the current user, Admin must provide hospital_id."""
    if request.user.role == 'Staff':
        return request.user.hospital
    elif request.user.role == 'Admin':
        hospital_id = request.GET.get('hospital_id')
        if hospital_id:
            return get_object_or_404(Hospital, id=hospital_id)
    return None


# =======================
# MEDICATION VIEWS
# =======================
@role_required('Admin', 'Staff')
def medication_list(request):
    hospital = get_user_hospital(request)
    if hospital:
        meds = Medication.objects.filter(hospital=hospital)
    else:
        meds = Medication.objects.all()

    return render(request, 'inventory/medication_list.html', {
        'medications': meds,
        'hospital': hospital
    })


@role_required('Admin', 'Staff')
def medication_create(request):
    hospital = get_user_hospital(request)
    if request.method == 'POST':
        if 'cancel' in request.POST:
            if request.user.role == 'Staff':
                return redirect('inventory:medication_list')
            else:
                return redirect(f"{reverse('inventory:medication_list')}?hospital_id={hospital.id}")
        form = MedicationForm(request.POST)
        if form.is_valid():
            med = form.save(commit=False)
            med.hospital = hospital
            med.save()
            messages.success(request, "Medication added to inventory.")
            return redirect('inventory:medication_list') if request.user.role == 'Staff' else redirect(f"{reverse('inventory:medication_list')}?hospital_id={hospital.id}")
    else:
        form = MedicationForm()

    return render(request, 'inventory/medication_form.html', {'form': form, 'hospital': hospital})


@role_required('Admin', 'Staff')
def medication_update(request, pk):
    med = get_object_or_404(Medication, pk=pk)
    hospital = med.hospital

    if request.user.role == 'Staff' and hospital != request.user.hospital:
        return redirect('inventory:medication_list')

    if request.method == 'POST':
        if 'cancel' in request.POST:
            return redirect('inventory:medication_list') if request.user.role == 'Staff' else redirect(f"{reverse('inventory:medication_list')}?hospital_id={hospital.id}")
        form = MedicationForm(request.POST, instance=med)
        if form.is_valid():
            med.save()
            messages.success(request, "Medication updated.")
            return redirect('inventory:medication_list') if request.user.role == 'Staff' else redirect(f"{reverse('inventory:medication_list')}?hospital_id={hospital.id}")
    else:
        form = MedicationForm(instance=med)

    return render(request, 'inventory/medication_form.html', {'form': form, 'hospital': hospital})


@role_required('Admin', 'Staff')
def medication_delete(request, pk):
    med = get_object_or_404(Medication, pk=pk)
    hospital = med.hospital

    if request.user.role == 'Staff' and hospital != request.user.hospital:
        return redirect('inventory:medication_list')

    if request.method == 'POST':
        med.delete()
        messages.success(request, "Medication removed from inventory.")
        return redirect('inventory:medication_list') if request.user.role == 'Staff' else redirect(f"{reverse('inventory:medication_list')}?hospital_id={hospital.id}")
    return render(request, 'inventory/medication_confirm_delete.html', {'medication': med, 'hospital': hospital})


# =======================
# MEDICAL SUPPLIES
# =======================
@role_required('Admin', 'Staff')
def supply_list(request):
    hospital = get_user_hospital(request)
    supplies = MedicalSupply.objects.filter(hospital=hospital) if hospital else MedicalSupply.objects.all()
    return render(request, 'inventory/supply_list.html', {'supplies': supplies, 'hospital': hospital})


@role_required('Admin', 'Staff')
def supply_create(request):
    hospital = get_user_hospital(request)
    if request.method == 'POST':
        if 'cancel' in request.POST:
            return redirect('inventory:supply_list') if request.user.role == 'Staff' else redirect(f"{reverse('inventory:supply_list')}?hospital_id={hospital.id}")
        form = MedicalSupplyForm(request.POST)
        if form.is_valid():
            supply = form.save(commit=False)
            supply.hospital = hospital
            supply.save()
            messages.success(request, "Medical supply added.")
            return redirect('inventory:supply_list') if request.user.role == 'Staff' else redirect(f"{reverse('inventory:supply_list')}?hospital_id={hospital.id}")
    else:
        form = MedicalSupplyForm()
    return render(request, 'inventory/supply_form.html', {'form': form, 'hospital': hospital})


@role_required('Admin', 'Staff')
def supply_update(request, pk):
    supply = get_object_or_404(MedicalSupply, pk=pk)
    hospital = supply.hospital
    if request.user.role == 'Staff' and hospital != request.user.hospital:
        return redirect('inventory:supply_list')
    if request.method == 'POST':
        if 'cancel' in request.POST:
            return redirect('inventory:supply_list') if request.user.role == 'Staff' else redirect(f"{reverse('inventory:supply_list')}?hospital_id={hospital.id}")
        form = MedicalSupplyForm(request.POST, instance=supply)
        if form.is_valid():
            form.save()
            messages.success(request, "Medical supply updated.")
            return redirect('inventory:supply_list') if request.user.role == 'Staff' else redirect(f"{reverse('inventory:supply_list')}?hospital_id={hospital.id}")
    else:
        form = MedicalSupplyForm(instance=supply)
    return render(request, 'inventory/supply_form.html', {'form': form, 'hospital': hospital})


@role_required('Admin', 'Staff')
def supply_delete(request, pk):
    supply = get_object_or_404(MedicalSupply, pk=pk)
    hospital = supply.hospital
    if request.user.role == 'Staff' and hospital != request.user.hospital:
        return redirect('inventory:supply_list')
    if request.method == 'POST':
        supply.delete()
        messages.success(request, "Medical supply deleted.")
        return redirect('inventory:supply_list') if request.user.role == 'Staff' else redirect(f"{reverse('inventory:supply_list')}?hospital_id={hospital.id}")
    return render(request, 'inventory/supply_confirm_delete.html', {'supply': supply, 'hospital': hospital})


# =======================
# EQUIPMENT
# =======================
@role_required('Admin', 'Staff')
def equipment_list(request):
    hospital = get_user_hospital(request)
    equipment = Equipment.objects.filter(hospital=hospital) if hospital else Equipment.objects.all()
    return render(request, 'inventory/equipment_list.html', {'equipment': equipment, 'hospital': hospital})

@role_required('Admin', 'Staff')
def equipment_create(request):
    hospital = get_user_hospital(request)
    if request.method == 'POST':
        if 'cancel' in request.POST:
            return redirect('inventory:equipment_list') if request.user.role == 'Staff' else redirect(f"{reverse('inventory:equipment_list')}?hospital_id={hospital.id}")
        form = EquipmentForm(request.POST)
        if form.is_valid():
            equip = form.save(commit=False)
            equip.hospital = hospital
            equip.save()
            messages.success(request, "Equipment added.")
            return redirect('inventory:equipment_list') if request.user.role == 'Staff' else redirect(f"{reverse('inventory:equipment_list')}?hospital_id={hospital.id}")
    else:
        form = EquipmentForm()
    return render(request, 'inventory/equipment_form.html', {'form': form, 'hospital': hospital})


@role_required('Admin', 'Staff')
def equipment_update(request, pk):
    equip = get_object_or_404(Equipment, pk=pk)
    hospital = equip.hospital
    if request.user.role == 'Staff' and hospital != request.user.hospital:
        return redirect('inventory:equipment_list')
    if request.method == 'POST':
        if 'cancel' in request.POST:
            return redirect('inventory:equipment_list') if request.user.role == 'Staff' else redirect(f"{reverse('inventory:equipment_list')}?hospital_id={hospital.id}")
        form = EquipmentForm(request.POST, instance=equip)
        if form.is_valid():
            form.save()
            messages.success(request, "Equipment updated.")
            return redirect('inventory:equipment_list') if request.user.role == 'Staff' else redirect(f"{reverse('inventory:equipment_list')}?hospital_id={hospital.id}")
    else:
        form = EquipmentForm(instance=equip)
    return render(request, 'inventory/equipment_form.html', {'form': form, 'hospital': hospital})


@role_required('Admin', 'Staff')
def equipment_delete(request, pk):
    equip = get_object_or_404(Equipment, pk=pk)
    hospital = equip.hospital
    if request.user.role == 'Staff' and hospital != request.user.hospital:
        return redirect('inventory:equipment_list')
    if request.method == 'POST':
        equip.delete()
        messages.success(request, "Equipment deleted.")
        return redirect('inventory:equipment_list') if request.user.role == 'Staff' else redirect(f"{reverse('inventory:equipment_list')}?hospital_id={hospital.id}")
    return render(request, 'inventory/equipment_confirm_delete.html', {'equipment': equip, 'hospital': hospital})
