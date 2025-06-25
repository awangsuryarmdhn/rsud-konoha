from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# ------------------------------
# Custom Pengguna
# ------------------------------
class Pengguna(AbstractUser):
    PERAN_CHOICES = (
        ('admin', 'Admin'),
        ('pasien', 'Pasien'),
        ('tenaga_medis', 'Tenaga Medis'),
    )
    peran = models.CharField(max_length=20, choices=PERAN_CHOICES)
    nama_lengkap = models.CharField(max_length=100)
    no_hp = models.CharField(max_length=20, blank=True, null=True)
    alamat = models.TextField(blank=True, null=True)
    nomor_rm = models.CharField(max_length=20, blank=True, null=True, unique=True)

    def __str__(self):
        return f"{self.username} ({self.peran})"

# ------------------------------
# Inventaris (gabungan Obat + Peralatan)
# ------------------------------
class Inventaris(models.Model):
    nama = models.CharField(max_length=100)
    jenis = models.CharField(max_length=50)  # contoh: Obat, Alat Medis, dll
    stok = models.IntegerField()
    satuan = models.CharField(max_length=20)
    keterangan = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nama

# ------------------------------
# Janji Temu
# ------------------------------
class JanjiTemu(models.Model):
    pasien = models.ForeignKey(Pengguna, on_delete=models.CASCADE, related_name='janji_pasien')
    tenaga_medis = models.ForeignKey(Pengguna, on_delete=models.CASCADE, limit_choices_to={'peran': 'tenaga_medis'})
    tanggal = models.DateField()
    jam = models.TimeField()
    keluhan = models.TextField()
    selesai = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.pasien.nama_lengkap} - {self.tenaga_medis.nama_lengkap} ({self.tanggal} {self.jam})"

# ------------------------------
# Rekam Medis + Laporan (digabung)
# ------------------------------
class RekamLaporan(models.Model):
    pasien = models.ForeignKey(Pengguna, on_delete=models.CASCADE, related_name='rekam_pasien')
    tenaga_medis = models.ForeignKey(Pengguna, on_delete=models.CASCADE, limit_choices_to={'peran': 'tenaga_medis'})
    tanggal = models.DateField(default=timezone.now)
    diagnosa = models.TextField()
    tindakan = models.TextField()
    resep = models.TextField(blank=True, null=True)
    catatan = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Rekam {self.pasien.nama_lengkap} - {self.tanggal}"

# ------------------------------
# Log Aktivitas Admin
# ------------------------------
class LogAktivitas(models.Model):
    pengguna = models.ForeignKey(Pengguna, on_delete=models.CASCADE)
    aksi = models.TextField()
    waktu = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.pengguna.username} - {self.aksi}"
