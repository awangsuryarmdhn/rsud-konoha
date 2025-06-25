from django.contrib import admin
from django import forms
from .models import Pengguna, Inventaris, JanjiTemu, RekamLaporan, LogAktivitas

# Custom form untuk Pengguna (Admin)
class PenggunaAdminForm(forms.ModelForm):
    password = forms.CharField(required=False, widget=forms.PasswordInput, help_text="Kosongkan jika tidak ingin mengubah password.")

    class Meta:
        model = Pengguna
        fields = '__all__'

    def save(self, commit=True):
        user = super().save(commit=False)
        pwd = self.cleaned_data.get("password")
        if pwd:
            user.set_password(pwd)
        elif user.pk:  # jika user sudah ada dan password tidak diubah
            existing = Pengguna.objects.get(pk=user.pk)
            user.password = existing.password
        if commit:
            user.save()
        return user

# Custom admin untuk Pengguna
@admin.register(Pengguna)
class PenggunaAdmin(admin.ModelAdmin):
    form = PenggunaAdminForm
    list_display = ('username', 'nama_lengkap', 'peran', 'no_hp', 'nomor_rm', 'is_active', 'is_staff')
    list_filter = ('peran', 'is_active')
    search_fields = ('username', 'nama_lengkap', 'no_hp', 'nomor_rm')
    list_editable = ('peran', 'is_active')

# Admin lain tetap
@admin.register(Inventaris)
class InventarisAdmin(admin.ModelAdmin):
    list_display = ('nama', 'jenis', 'stok', 'satuan')
    search_fields = ('nama', 'jenis')
    list_filter = ('jenis',)
    list_editable = ('stok',)

@admin.register(JanjiTemu)
class JanjiTemuAdmin(admin.ModelAdmin):
    list_display = ('pasien', 'tenaga_medis', 'tanggal', 'jam', 'keluhan', 'selesai')
    search_fields = ('pasien__nama_lengkap', 'tenaga_medis__nama_lengkap', 'keluhan')
    list_filter = ('selesai', 'tanggal')
    list_editable = ('selesai',)

@admin.register(RekamLaporan)
class RekamLaporanAdmin(admin.ModelAdmin):
    list_display = ('pasien', 'tenaga_medis', 'tanggal', 'diagnosa', 'tindakan')
    search_fields = ('pasien__nama_lengkap', 'tenaga_medis__nama_lengkap', 'diagnosa', 'tindakan')
    list_filter = ('tanggal',)

@admin.register(LogAktivitas)
class LogAktivitasAdmin(admin.ModelAdmin):
    list_display = ('pengguna', 'aksi', 'waktu')
    search_fields = ('pengguna__username', 'aksi')
    list_filter = ('waktu',)
