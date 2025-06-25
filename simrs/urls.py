from django.urls import path
from . import views

urlpatterns = [
    # Autentikasi
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('daftar/', views.daftar_pasien, name='daftar_pasien'),

    # Redirector
    path('dashboard/', views.dashboard, name='dashboard'),

    # Dashboard dipisah sesuai role
    path('dashboard-admin/', views.dashboard_admin, name='dashboard_admin'),
    path('dashboard-pasien/', views.dashboard_pasien, name='dashboard_pasien'),
    path('dashboard-medis/', views.dashboard_medis, name='dashboard_medis'),

    # AJAX
    path('ajax/cek-username/', views.cek_username_ajax, name='cek_username_ajax'),
    path('ajax/cek-jadwal/', views.cek_jadwal_dokter, name='cek_jadwal_dokter'),

    # Janji Temu
    path('buat-janji/', views.buat_janji_temu, name='buat_janji_temu'),
    path('rekam-medis/', views.input_rekam_medis, name='input_rekam_medis'),

    # Inventaris
    path('inventaris/', views.inventaris_admin, name='inventaris_admin'),
    path('inventaris/tambah/', views.tambah_inventaris, name='tambah_inventaris'),
    path('inventaris/hapus/<int:pk>/', views.hapus_inventaris, name='hapus_inventaris'),

    # Laporan & Export
    path('laporan/', views.laporan_pdf, name='laporan_pdf'),

    # Log Aktivitas
    path('log-aktivitas/', views.log_aktivitas, name='log_aktivitas'),

    # Dokumentasi & Panduan
    path('panduan/', views.panduan_penggunaan, name='panduan_penggunaan'),
    path('dokumentasi/', views.dokumentasi_sistem, name='dokumentasi_sistem'),
]
