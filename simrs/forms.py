from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Pengguna, Inventaris, JanjiTemu, RekamLaporan

# ------------------------------
# Registrasi Pasien
# ------------------------------
class PasienRegisterForm(UserCreationForm):
    class Meta:
        model = Pengguna
        fields = ['username', 'nama_lengkap', 'no_hp', 'alamat', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.peran = 'pasien'
        user.nomor_rm = self.generate_rm()
        if commit:
            user.save()
        return user

    def generate_rm(self):
        import random
        from datetime import datetime
        prefix = datetime.now().strftime('%Y%m%d')
        rand = random.randint(1000, 9999)
        return f'RM{prefix}{rand}'

# ------------------------------
# Form Janji Temu
# ------------------------------
class JanjiTemuForm(forms.ModelForm):
    class Meta:
        model = JanjiTemu
        fields = ['tenaga_medis', 'tanggal', 'jam', 'keluhan']
        widgets = {
            'tanggal': forms.DateInput(attrs={'type': 'date', 'class': 'input input-bordered'}),
            'jam': forms.TimeInput(attrs={'type': 'time', 'class': 'input input-bordered'}),
            'keluhan': forms.Textarea(attrs={'class': 'textarea textarea-bordered'}),
        }

# ------------------------------
# Form Inventaris
# ------------------------------
class InventarisForm(forms.ModelForm):
    class Meta:
        model = Inventaris
        fields = ['nama', 'jenis', 'stok', 'satuan', 'keterangan']
        widgets = {
            'nama': forms.TextInput(attrs={'class': 'input input-bordered'}),
            'jenis': forms.TextInput(attrs={'class': 'input input-bordered'}),
            'stok': forms.NumberInput(attrs={'class': 'input input-bordered'}),
            'satuan': forms.TextInput(attrs={'class': 'input input-bordered'}),
            'keterangan': forms.Textarea(attrs={'class': 'textarea textarea-bordered'}),
        }

# ------------------------------
# Form Rekam Medis
# ------------------------------
class RekamMedisForm(forms.ModelForm):
    class Meta:
        model = RekamLaporan
        fields = ['diagnosa', 'tindakan', 'resep', 'catatan']
        widgets = {
            'diagnosa': forms.Textarea(attrs={'class': 'textarea textarea-bordered'}),
            'tindakan': forms.Textarea(attrs={'class': 'textarea textarea-bordered'}),
            'resep': forms.Textarea(attrs={'class': 'textarea textarea-bordered'}),
            'catatan': forms.Textarea(attrs={'class': 'textarea textarea-bordered'}),
        }
