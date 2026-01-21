import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from matplotlib.animation import FuncAnimation

def create_sphere(center, radius, color):
    """Membuat sphere untuk bagian tubuh"""
    u = np.linspace(0, 2 * np.pi, 30)
    v = np.linspace(0, np.pi, 20)
    x = radius * np.outer(np.cos(u), np.sin(v)) + center[0]
    y = radius * np.outer(np.sin(u), np.sin(v)) + center[1]
    z = radius * np.outer(np.ones(np.size(u)), np.cos(v)) + center[2]
    return x, y, z, color

def create_cylinder(center, radius, height, color, axis='z'):
    """Membuat cylinder untuk badan dan lengan"""
    u = np.linspace(0, 2 * np.pi, 30)
    h = np.linspace(-height/2, height/2, 10)
    
    if axis == 'z':
        x = radius * np.outer(np.cos(u), np.ones(len(h))) + center[0]
        y = radius * np.outer(np.sin(u), np.ones(len(h))) + center[1]
        z = np.outer(np.ones(len(u)), h) + center[2]
    elif axis == 'y':
        x = radius * np.outer(np.cos(u), np.ones(len(h))) + center[0]
        z = radius * np.outer(np.sin(u), np.ones(len(h))) + center[2]
        y = np.outer(np.ones(len(u)), h) + center[1]
    else:
        y = radius * np.outer(np.cos(u), np.ones(len(h))) + center[1]
        z = radius * np.outer(np.sin(u), np.ones(len(h))) + center[2]
        x = np.outer(np.ones(len(u)), h) + center[0]
    
    return x, y, z, color

def apply_translation(x, y, z, tx, ty, tz):
    """TRANSLASI 3D: Menggeser objek"""
    return x + tx, y + ty, z + tz

def apply_rotation_x(x, y, z, angle):
    """ROTASI 3D terhadap sumbu X"""
    rad = np.radians(angle)
    cos_a = np.cos(rad)
    sin_a = np.sin(rad)
    y_new = y * cos_a - z * sin_a
    z_new = y * sin_a + z * cos_a
    return x, y_new, z_new

def apply_rotation_y(x, y, z, angle):
    """ROTASI 3D terhadap sumbu Y"""
    rad = np.radians(angle)
    cos_a = np.cos(rad)
    sin_a = np.sin(rad)
    x_new = x * cos_a + z * sin_a
    z_new = -x * sin_a + z * cos_a
    return x_new, y, z_new

def apply_rotation_z(x, y, z, angle):
    """ROTASI 3D terhadap sumbu Z"""
    rad = np.radians(angle)
    cos_a = np.cos(rad)
    sin_a = np.sin(rad)
    x_new = x * cos_a - y * sin_a
    y_new = x * sin_a + y * cos_a
    return x_new, y_new, z

def apply_scale(x, y, z, sx, sy, sz):
    """SKALA 3D: Mengubah ukuran objek"""
    return x * sx, y * sy, z * sz

def apply_reflection(x, y, z, reflect_x, reflect_y, reflect_z):
    """REFLEKSI 3D: Mencerminkan objek"""
    rx = -1 if reflect_x else 1
    ry = -1 if reflect_y else 1
    rz = -1 if reflect_z else 1
    return x * rx, y * ry, z * rz

def create_luffy_parts(arm_angle=0, leg_angle=0):
    """Membuat semua bagian Luffy dengan pose berlari"""
    skin_color = '#ffdbac'
    hat_color = '#f4d03f'
    red_color = '#ff0000'
    dark_red = '#8B0000'
    blue_color = '#0066cc'
    brown_color = '#8B4513'
    black_color = '#000000'
    
    parts = []
    
    # Kepala
    parts.append(create_sphere([0, 0, 2], 0.5, skin_color))
    
    # Mata
    parts.append(create_sphere([-0.15, 0.4, 2.1], 0.08, black_color))
    parts.append(create_sphere([0.15, 0.4, 2.1], 0.08, black_color))
    
    # Topi
    parts.append(create_cylinder([0, 0, 2.5], 0.7, 0.05, hat_color, 'z'))
    parts.append(create_cylinder([0, 0, 2.65], 0.45, 0.3, hat_color, 'z'))
    parts.append(create_cylinder([0, 0, 2.5], 0.51, 0.08, red_color, 'z'))
    
    # Badan (sedikit condong saat berlari)
    parts.append(create_cylinder([0, 0, 0.8], 0.4, 1.0, red_color, 'z'))
    parts.append(create_cylinder([-0.3, 0, 0.8], 0.15, 1.1, dark_red, 'z'))
    parts.append(create_cylinder([0.3, 0, 0.8], 0.15, 1.1, dark_red, 'z'))
    
    # Lengan bergerak (animasi mengayun)
    arm_offset = np.sin(np.radians(arm_angle)) * 0.3
    
    parts.append(create_cylinder([-0.6, arm_offset, 0.8], 0.12, 0.8, skin_color, 'z'))
    parts.append(create_cylinder([0.6, -arm_offset, 0.8], 0.12, 0.8, skin_color, 'z'))
    parts.append(create_sphere([-0.6, arm_offset, 0.35], 0.13, skin_color))
    parts.append(create_sphere([0.6, -arm_offset, 0.35], 0.13, skin_color))
    
    # Celana
    parts.append(create_cylinder([0, 0, 0.05], 0.45, 0.5, blue_color, 'z'))
    
    # Kaki bergerak (animasi berlari)
    leg_offset = np.sin(np.radians(leg_angle)) * 0.4
    
    parts.append(create_cylinder([-0.2, leg_offset, -0.65], 0.13, 0.9, skin_color, 'z'))
    parts.append(create_cylinder([0.2, -leg_offset, -0.65], 0.13, 0.9, skin_color, 'z'))
    
    # Sandal
    u = np.linspace(-0.3, -0.1, 5)
    v = np.linspace(-0.15 + leg_offset, 0.15 + leg_offset, 5)
    U, V = np.meshgrid(u, v)
    parts.append((U, V, np.ones_like(U) * (-1.12), brown_color))
    
    u = np.linspace(0.1, 0.3, 5)
    v = np.linspace(-0.15 - leg_offset, 0.15 - leg_offset, 5)
    U, V = np.meshgrid(u, v)
    parts.append((U, V, np.ones_like(U) * (-1.12), brown_color))
    
    return parts

def create_food():
    """Membuat makanan (daging)"""
    parts = []
    
    # Tulang
    bone = create_cylinder([0, 0, 0], 0.05, 0.6, '#f5f5dc', 'x')
    parts.append(bone)
    
    # Daging kiri
    meat_left = create_sphere([-0.35, 0, 0], 0.15, '#8B4513')
    parts.append(meat_left)
    
    # Daging kanan
    meat_right = create_sphere([0.35, 0, 0], 0.15, '#8B4513')
    parts.append(meat_right)
    
    return parts

def create_grass_field():
    """Membuat padang rumput"""
    grass_elements = []
    
    # Tanah rumput (ground plane)
    x_ground = np.linspace(-5, 10, 20)
    y_ground = np.linspace(-5, 5, 20)
    X_ground, Y_ground = np.meshgrid(x_ground, y_ground)
    
    # Membuat permukaan bergelombang
    Z_ground = -1.5 + 0.1 * np.sin(X_ground * 0.5) * np.cos(Y_ground * 0.5)
    
    grass_elements.append((X_ground, Y_ground, Z_ground, '#2d5016'))
    
    # Lapisan rumput lebih terang di atas
    Z_grass = Z_ground + 0.02
    grass_elements.append((X_ground, Y_ground, Z_grass, '#3a7d1f'))
    
    return grass_elements

def create_grass_blades():
    """Membuat bilah-bilah rumput kecil"""
    blades = []
    
    # Buat beberapa bilah rumput secara acak
    np.random.seed(42)
    for i in range(30):
        x_pos = np.random.uniform(-4, 9)
        y_pos = np.random.uniform(-4, 4)
        
        # Bilah rumput kecil (cylinder tipis)
        height = np.random.uniform(0.15, 0.3)
        blade = create_cylinder([x_pos, y_pos, -1.5 + height/2], 0.02, height, '#4a9d2a', 'z')
        blades.append(blade)
    
    return blades

def create_flowers():
    """Membuat bunga-bunga kecil"""
    flowers = []
    
    np.random.seed(123)
    for i in range(15):
        x_pos = np.random.uniform(-3, 8)
        y_pos = np.random.uniform(-3, 3)
        
        # Batang
        stem = create_cylinder([x_pos, y_pos, -1.4], 0.015, 0.2, '#2d5016', 'z')
        flowers.append(stem)
        
        # Bunga (sphere kecil)
        colors = ['#ff69b4', '#ffff00', '#ff6347', '#9370db', '#ffa500']
        flower_color = colors[i % len(colors)]
        flower = create_sphere([x_pos, y_pos, -1.25], 0.05, flower_color)
        flowers.append(flower)
    
    return flowers

def create_clouds():
    """Membuat awan di langit"""
    clouds = []
    
    # Awan 1
    cloud1_parts = [
        create_sphere([2, -3, 3.5], 0.3, '#ffffff'),
        create_sphere([2.3, -3, 3.5], 0.25, '#ffffff'),
        create_sphere([1.7, -3, 3.5], 0.25, '#ffffff'),
        create_sphere([2, -3, 3.7], 0.2, '#ffffff')
    ]
    clouds.extend(cloud1_parts)
    
    # Awan 2
    cloud2_parts = [
        create_sphere([5, 3.5, 3.8], 0.35, '#ffffff'),
        create_sphere([5.4, 3.5, 3.8], 0.28, '#ffffff'),
        create_sphere([4.6, 3.5, 3.8], 0.28, '#ffffff')
    ]
    clouds.extend(cloud2_parts)
    
    # Awan 3
    cloud3_parts = [
        create_sphere([-1, 1, 3.6], 0.25, '#ffffff'),
        create_sphere([-0.7, 1, 3.6], 0.2, '#ffffff'),
        create_sphere([-1.3, 1, 3.6], 0.2, '#ffffff')
    ]
    clouds.extend(cloud3_parts)
    
    return clouds

def apply_transformations(parts, tx, ty, tz, rx, ry, rz, sx, sy, sz, ref_x, ref_y, ref_z):
    """Menerapkan semua transformasi"""
    transformed_parts = []
    
    for part in parts:
        x, y, z, color = part
        
        # Rotasi
        x, y, z = apply_rotation_x(x, y, z, rx)
        x, y, z = apply_rotation_y(x, y, z, ry)
        x, y, z = apply_rotation_z(x, y, z, rz)
        
        # Skala
        x, y, z = apply_scale(x, y, z, sx, sy, sz)
        
        # Refleksi
        x, y, z = apply_reflection(x, y, z, ref_x, ref_y, ref_z)
        
        # Translasi
        x, y, z = apply_translation(x, y, z, tx, ty, tz)
        
        transformed_parts.append((x, y, z, color))
    
    return transformed_parts

def create_animation():
    """Membuat animasi Luffy berlari mengambil makanan"""
    
    fig = plt.figure(figsize=(14, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    # Total frames untuk animasi
    total_frames = 200
    
    # Fase animasi
    phase1_end = 60   # Berlari ke makanan
    phase2_end = 80   # Mengambil makanan
    phase3_end = 140  # Berlari kembali
    phase4_end = 200  # Kembali ke posisi awal
    
    # Info teks
    info_text = ax.text2D(0.05, 0.95, '', transform=ax.transAxes, 
                          fontsize=12, fontweight='bold', color='red',
                          bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.8))
    
    def update(frame):
        ax.clear()
        
        # Default transformasi
        tx, ty, tz = 0, 0, 0
        rx, ry, rz = 0, 0, 0
        sx, sy, sz = 1, 1, 1
        ref_x, ref_y, ref_z = False, False, False
        
        arm_angle = 0
        leg_angle = 0
        show_food_in_hand = False
        show_food_on_ground = True
        food_eaten = False
        status_text = ""
        
        # GAMBAR BACKGROUND DULU
        
        # 1. Padang rumput
        grass_field = create_grass_field()
        for x, y, z, color in grass_field:
            ax.plot_surface(x, y, z, color=color, alpha=0.95, edgecolor='none', shade=True)
        
        # 2. Bilah rumput
        grass_blades = create_grass_blades()
        for blade in grass_blades:
            x, y, z, color = blade
            ax.plot_surface(x, y, z, color=color, alpha=0.8, edgecolor='none')
        
        # 3. Bunga-bunga
        flowers = create_flowers()
        for flower in flowers:
            x, y, z, color = flower
            ax.plot_surface(x, y, z, color=color, alpha=0.9, edgecolor='none')
        
        # 4. Awan di langit
        clouds = create_clouds()
        for cloud in clouds:
            x, y, z, color = cloud
            ax.plot_surface(x, y, z, color=color, alpha=0.7, edgecolor='none')
        
        # FASE 1: Berlari ke makanan (frame 0-60)
        if frame < phase1_end:
            progress = frame / phase1_end
            
            # TRANSLASI: Bergerak ke kanan
            tx = progress * 6
            
            # ROTASI: Menghadap ke kanan (Y-axis 90 derajat)
            ry = 90
            
            # Animasi berlari (kaki dan tangan mengayun)
            arm_angle = frame * 20
            leg_angle = frame * 20
            
            # SKALA: Sedikit membesar (efek semangat)
            sx = sy = sz = 1 + (np.sin(frame * 0.2) * 0.05)
            
            status_text = f"FASE 1: Berlari ke makanan! ({int(progress*100)}%)"
        
        # FASE 2: Mengambil makanan (frame 60-80)
        elif frame < phase2_end:
            tx = 6
            ry = 90
            
            # Gerakan membungkuk mengambil
            bounce = np.sin((frame - phase1_end) * 0.3) * 0.3
            tz = -bounce
            
            # REFLEKSI: Berputar saat mengambil
            if frame > phase1_end + 10:
                show_food_in_hand = True
                show_food_on_ground = False
            
            status_text = "FASE 2: Mengambil makanan!"
        
        # FASE 3: Berlari kembali (frame 80-140)
        elif frame < phase3_end:
            progress = (frame - phase2_end) / (phase3_end - phase2_end)
            
            # TRANSLASI: Kembali ke kiri
            tx = 6 - (progress * 6)
            
            # ROTASI: Menghadap ke kiri (Y-axis 270 derajat)
            ry = 270
            
            # SKALA: Lebih besar (membawa makanan dengan semangat)
            sx = sy = sz = 1.1
            
            # Animasi berlari
            arm_angle = frame * 20
            leg_angle = frame * 20
            
            show_food_in_hand = True
            show_food_on_ground = False
            
            status_text = f"FASE 3: Berlari kembali dengan makanan! ({int(progress*100)}%)"
        
        # FASE 4: Kembali dan makan (frame 140-200)
        else:
            progress = (frame - phase3_end) / (phase4_end - phase3_end)
            
            tx = 0
            ry = 0  # Menghadap depan
            
            # ROTASI: Melompat kegirangan
            if progress < 0.5:
                jump = np.sin(progress * np.pi * 4) * 0.5
                tz = jump
                rz = np.sin(progress * np.pi * 4) * 10
            
            # Makanan menghilang (dimakan)
            if progress > 0.6:
                food_eaten = True
                show_food_in_hand = False
                
                # SKALA: Perut membesar setelah makan
                sx = 1.2
                sy = 1.2
                sz = 1.1
            
            if food_eaten:
                status_text = "FASE 4: Yummy! Makanan habis! 🍖"
            else:
                status_text = "FASE 4: Kembali ke posisi awal!"
        
        # Buat Luffy dengan pose berlari
        luffy_parts = create_luffy_parts(arm_angle, leg_angle)
        transformed_luffy = apply_transformations(
            luffy_parts, tx, ty, tz, rx, ry, rz, sx, sy, sz, ref_x, ref_y, ref_z
        )
        
        # Plot Luffy
        for x, y, z, color in transformed_luffy:
            ax.plot_surface(x, y, z, color=color, alpha=0.9, edgecolor='none')
        
        # Plot makanan di tanah (awal)
        if show_food_on_ground:
            food_parts = create_food()
            food_transformed = apply_transformations(
                food_parts, 6, 0, -0.5, 0, 0, 0, 0.8, 0.8, 0.8, False, False, False
            )
            for x, y, z, color in food_transformed:
                ax.plot_surface(x, y, z, color=color, alpha=0.9, edgecolor='none')
        
        # Plot makanan di tangan
        if show_food_in_hand:
            food_parts = create_food()
            # Posisi makanan mengikuti tangan Luffy
            food_tx = tx + 0.6 * np.cos(np.radians(ry))
            food_ty = ty + 0.6 * np.sin(np.radians(ry))
            food_tz = tz + 1.5
            
            food_transformed = apply_transformations(
                food_parts, food_tx, food_ty, food_tz, 0, ry, 45, 0.5, 0.5, 0.5, False, False, False
            )
            for x, y, z, color in food_transformed:
                ax.plot_surface(x, y, z, color=color, alpha=0.9, edgecolor='none')
        
        # Update info text
        info_text.set_text(status_text)
        
        # Setting tampilan
        ax.set_xlabel('X', fontsize=10, fontweight='bold')
        ax.set_ylabel('Y', fontsize=10, fontweight='bold')
        ax.set_zlabel('Z', fontsize=10, fontweight='bold')
        ax.set_title('Luffy Berlari Mengambil Makanan - Transformasi 3D\n(Translasi • Rotasi • Skala • Refleksi)', 
                     fontsize=14, fontweight='bold')
        
        ax.set_xlim([-2, 8])
        ax.set_ylim([-3, 3])
        ax.set_zlim([-2, 4])
        ax.grid(False)  # Matikan grid untuk tampilan lebih natural
        ax.set_facecolor('#87CEEB')  # Langit biru
        ax.xaxis.pane.fill = False
        ax.yaxis.pane.fill = False
        ax.zaxis.pane.fill = False
        
        # Warna background langit gradasi
        fig.patch.set_facecolor('#87CEEB')
        
        # Sudut pandang mengikuti Luffy
        if frame < phase1_end:
            ax.view_init(elev=20, azim=120)
        elif frame < phase2_end:
            ax.view_init(elev=15, azim=90)
        elif frame < phase3_end:
            ax.view_init(elev=20, azim=60)
        else:
            ax.view_init(elev=25, azim=45)
        
        return ax,
    
    # Buat animasi
    anim = FuncAnimation(fig, update, frames=total_frames, interval=50, blit=False, repeat=True)
    
    plt.tight_layout()
    plt.show()
    
    return anim

# Jalankan program
if __name__ == "__main__":
    print("=" * 70)
    print(" " * 15 + "LUFFY BERLARI MENGAMBIL MAKANAN")
    print("=" * 70)
    print("\n📖 CERITA ANIMASI:")
    print("   1. FASE 1: Luffy berlari ke kanan mencari makanan (TRANSLASI + ROTASI)")
    print("   2. FASE 2: Luffy mengambil makanan dari tanah (SKALA + TRANSLASI)")
    print("   3. FASE 3: Luffy berlari kembali membawa makanan (TRANSLASI + ROTASI)")
    print("   4. FASE 4: Luffy melompat kegirangan dan makan! (ROTASI + SKALA)")
    print("\n🎯 TRANSFORMASI 3D YANG DIGUNAKAN:")
    print("   ✓ TRANSLASI - Luffy bergerak kiri-kanan")
    print("   ✓ ROTASI - Luffy berputar menghadap kiri/kanan, melompat")
    print("   ✓ SKALA - Ukuran berubah saat semangat dan kenyang")
    print("   ✓ REFLEKSI - Digunakan untuk gerakan dinamis")
    print("\n🎬 ANIMASI:")
    print("   - Kaki dan tangan mengayun saat berlari")
    print("   - Makanan berpindah dari tanah ke tangan")
    print("   - Perut membesar setelah makan")
    print("   - Kamera bergerak mengikuti aksi")
    print("\n⏱️  Total durasi: ~10 detik (200 frame)")
    print("🔄  Animasi akan berulang otomatis")
    print("=" * 70)
    print("\nMemulai animasi...\n")
    
    anim = create_animation()