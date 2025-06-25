from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
from django.template.loader import render_to_string
import pdfkit

from .models import *
from .forms import *

# -----------------------------------
# Autentikasi
# -----------------------------------
def login_view(request):
    if request.method == 'POST':
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Username atau password salah.")
    return render(request, 'simrs/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

# -----------------------------------
# Redirector Dashboard
# -----------------------------------
@login_required
def dashboard(request):
    # Pastikan user memiliki peran yang valid
    if not hasattr(request.user, 'peran') or request.user.peran not in ['admin', 'tenaga_medis', 'pasien']:
        logout(request)
        messages.error(request, "Akun tidak memiliki peran valid. Silakan login ulang.")
        return redirect('login')
    # Arahkan ke dashboard sesuai peran
    if request.user.peran == 'admin':
        return redirect('dashboard_admin')
    elif request.user.peran == 'tenaga_medis':
        return redirect('dashboard_medis')
    elif request.user.peran == 'pasien':
        return redirect('dashboard_pasien')

# -----------------------------------
# Dashboard Admin
# -----------------------------------
@login_required
def dashboard_admin(request):
    if request.user.peran != 'admin':
        messages.error(request, "Anda tidak punya akses ke dashboard admin.")
        return redirect('dashboard')
    total_pasien = Pengguna.objects.filter(peran='pasien').count()
    total_dokter = Pengguna.objects.filter(peran='tenaga_medis').count()
    total_inventaris = Inventaris.objects.count()
    return render(request, 'simrs/dashboard_admin.html', {
        'total_pasien': total_pasien,
        'total_dokter': total_dokter,
        'total_inventaris': total_inventaris,
    })

# -----------------------------------
# Dashboard Tenaga Medis
# -----------------------------------
@login_required
def dashboard_medis(request):
    if request.user.peran != 'tenaga_medis':
        messages.error(request, "Anda tidak punya akses ke dashboard medis.")
        return redirect('dashboard')
    janji = JanjiTemu.objects.filter(
        tenaga_medis=request.user, tanggal=timezone.now().date()
    ).order_by('jam')
    return render(request, 'simrs/dashboard_medis.html', {'janji_list': janji})

# -----------------------------------
# Dashboard Pasien
# -----------------------------------
@login_required
def dashboard_pasien(request):
    if request.user.peran != 'pasien':
        messages.error(request, "Anda tidak punya akses ke dashboard pasien.")
        return redirect('dashboard')
    janji = JanjiTemu.objects.filter(pasien=request.user)
    return render(request, 'simrs/dashboard_pasien.html', {'janji_list': janji})

# -----------------------------------
# Pendaftaran Pasien
# -----------------------------------
def daftar_pasien(request):
    if request.method == 'POST':
        form = PasienRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Berhasil mendaftar. Silakan login.")
            return redirect('login')
    else:
        form = PasienRegisterForm()
    return render(request, 'simrs/daftar_pasien.html', {'form': form})

# -----------------------------------
# AJAX: Validasi Username
# -----------------------------------
def cek_username_ajax(request):
    username = request.GET.get('username')
    exists = Pengguna.objects.filter(username=username).exists()
    return JsonResponse({'exists': exists})

# -----------------------------------
# AJAX: Validasi Jadwal Dokter
# -----------------------------------
@login_required
def cek_jadwal_dokter(request):
    dokter_id = request.GET.get('dokter')
    tanggal = request.GET.get('tanggal')
    jam = request.GET.get('jam')
    bentrok = JanjiTemu.objects.filter(
        tenaga_medis_id=dokter_id,
        tanggal=tanggal,
        jam=jam
    ).exists()
    return JsonResponse({'bentrok': bentrok})

# -----------------------------------
# Janji Temu
# -----------------------------------
@login_required
def buat_janji_temu(request):
    if request.method == 'POST':
        form = JanjiTemuForm(request.POST)
        if form.is_valid():
            janji = form.save(commit=False)
            janji.pasien = request.user
            janji.save()
            messages.success(request, "Janji temu berhasil dibuat!")
            return redirect('dashboard')
    else:
        form = JanjiTemuForm()
    return render(request, 'simrs/buat_janji_temu.html', {'form': form})

# -----------------------------------
# Input Rekam Medis
# -----------------------------------
@login_required
def input_rekam_medis(request, id_janji):
    janji = get_object_or_404(JanjiTemu, id=id_janji)
    if request.method == 'POST':
        form = RekamMedisForm(request.POST)
        if form.is_valid():
            rekam = form.save(commit=False)
            rekam.pasien = janji.pasien
            rekam.tenaga_medis = request.user
            rekam.save()
            janji.selesai = True
            janji.save()
            messages.success(request, "Rekam medis berhasil disimpan.")
            return redirect('dashboard')
    else:
        form = RekamMedisForm()
    return render(request, 'simrs/rekam_medis_input.html', {'form': form, 'janji': janji})

# -----------------------------------
# Inventaris CRUD
# -----------------------------------
@login_required
def inventaris_admin(request):
    q = request.GET.get('q')
    if q:
        inventaris = Inventaris.objects.filter(Q(nama__icontains=q) | Q(jenis__icontains=q))
    else:
        inventaris = Inventaris.objects.all()
    return render(request, 'simrs/inventaris_admin.html', {'inventaris': inventaris, 'query': q})

@login_required
def tambah_inventaris(request):
    if request.method == 'POST':
        form = InventarisForm(request.POST)
        if form.is_valid():
            item = form.save()
            LogAktivitas.objects.create(pengguna=request.user, aksi=f"Menambah inventaris: {item.nama}")
            messages.success(request, "Data berhasil ditambahkan.")
            return redirect('inventaris_admin')
    else:
        form = InventarisForm()
    return render(request, 'simrs/inventaris_form.html', {'form': form})

@login_required
def hapus_inventaris(request, pk):
    item = get_object_or_404(Inventaris, pk=pk)
    LogAktivitas.objects.create(pengguna=request.user, aksi=f"Menghapus inventaris: {item.nama}")
    item.delete()
    messages.success(request, "Data berhasil dihapus.")
    return redirect('inventaris_admin')

# -----------------------------------
# Laporan PDF
# -----------------------------------
@login_required
def laporan_pdf(request):
    data = RekamLaporan.objects.all()
    html = render_to_string("simrs/laporan_pdf.html", {'data': data})
    pdf = pdfkit.from_string(html, False)
    return HttpResponse(pdf, content_type='application/pdf')

# -----------------------------------
# Log Aktivitas Admin
# -----------------------------------
@login_required
def log_aktivitas(request):
    if request.user.peran != 'admin':
        return redirect('dashboard')
    logs = LogAktivitas.objects.all().order_by('-waktu')
    return render(request, 'simrs/log_aktivitas.html', {'log_list': logs})

# -----------------------------------
# Dokumentasi dan Panduan
# -----------------------------------
@login_required
def panduan_penggunaan(request):
    return render(request, 'simrs/panduan_penggunaan.html')

@login_required
def dokumentasi_sistem(request):
    return render(request, 'simrs/dokumentasi.html')
