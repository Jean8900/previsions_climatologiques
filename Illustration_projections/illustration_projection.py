"""
Script de visualisation comparative des projections cartographiques
====================================================================
Objectif : Démontrer l'impact du choix de projection sur l'interprétation
          des données climatologiques globales.

Auteur : SCP - Prévisions Climatologiques
Contexte : Analyse de données ERA5-Land, WorldClim, CHIRPS, MSWEP
"""

# ==============================================================================
# IMPORTS
# ==============================================================================
import cartopy.crs as ccrs           # Systèmes de coordonnées et projections
import cartopy.feature as cfeature   # Caractéristiques géographiques
import matplotlib.pyplot as plt      # Visualisation
import numpy as np                   # Calculs numériques

print("Merci de patienter, le run prend environ 2 minutes")

# ==============================================================================
# CONFIGURATION DE LA FIGURE
# ==============================================================================
# Création de 2 subplots pour comparaison côte à côte
# Initialisation avec projection PlateCarree par défaut
fig, axes = plt.subplots(2, 1, figsize=(18, 14),
                          subplot_kw={'projection': ccrs.PlateCarree()})

# Modification de la projection du second subplot vers Robinson
# Robinson = compromis optimal entre préservation des surfaces et des formes
axes[1] = plt.subplot(2, 1, 2, projection=ccrs.Robinson())

# Titre général de la figure
fig.suptitle('Impact des Projections Cartographiques sur l\'Analyse Climatologique',
             fontsize=18, fontweight='bold', y=0.98)

# ==============================================================================
# GÉNÉRATION DES DONNÉES CLIMATIQUES SYNTHÉTIQUES
# ==============================================================================
# Création d'une grille longitude/latitude couvrant le globe
lons = np.linspace(-180, 180, 360)  # 360 points de longitude
lats = np.linspace(-90, 90, 180)    # 180 points de latitude
lon_grid, lat_grid = np.meshgrid(lons, lats)

# Simulation d'anomalies de température réalistes
# Modélisation du réchauffement amplifié aux pôles (Arctic amplification)
temp_anomaly = 2.5 * (1 + 0.8 * np.abs(np.sin(np.radians(lat_grid))))
# Ajout de variations longitudinales
temp_anomaly += 0.5 * np.cos(np.radians(lon_grid)) * np.sin(np.radians(lat_grid))
# Ajout de bruit pour simuler la variabilité naturelle
temp_anomaly += 0.3 * np.random.randn(180, 360)

# ==============================================================================
# CARTE 1 : PROJECTION PLATECARREE (CYLINDRIQUE ÉQUIRECTANGULAIRE)
# ==============================================================================
# Cette projection est la plus simple mais déforme significativement les surfaces
# aux hautes latitudes (ex: Groenland apparaît surdimensionné)
ax1 = axes[0]
ax1.set_title('Projection PlateCarree (Cylindrique Équirectangulaire)\n' +
              '⚠️ Distorsions importantes aux hautes latitudes - Groenland surdimensionné',
              fontsize=13, fontweight='bold', pad=15, color='darkred')

# Ajout des couches géographiques de base
ax1.add_feature(cfeature.LAND, facecolor='lightgray', edgecolor='black', linewidth=0.3)
ax1.add_feature(cfeature.OCEAN, facecolor='#e6f2ff')
ax1.add_feature(cfeature.COASTLINE, linewidth=0.5, edgecolor='black')
ax1.add_feature(cfeature.BORDERS, linewidth=0.3, edgecolor='gray', alpha=0.5)

# Visualisation des anomalies de température
# RdYlBu_r = palette rouge-jaune-bleu inversée (rouge = chaud, bleu = froid)
# vmin/vmax fixés pour permettre la comparaison entre les deux cartes
im1 = ax1.contourf(lon_grid, lat_grid, temp_anomaly,
                   levels=15, cmap='RdYlBu_r',
                   transform=ccrs.PlateCarree(),
                   alpha=0.75, vmin=0, vmax=5)

# Ajout d'une grille avec labels de coordonnées
gl1 = ax1.gridlines(draw_labels=True, linewidth=0.5, color='gray',
                    alpha=0.5, linestyle='--')
gl1.top_labels = False      # Désactivation des labels en haut
gl1.right_labels = False    # Désactivation des labels à droite

# Zones géographiques d'exemple pour faciliter la comparaison visuelle
# Format : (longitude, latitude, label)
zones_exemple = [
    (-80, 10, 'Zone\nTropicale'),
    (20, -20, 'Afrique'),
    (100, 50, 'Asie\nCentrale'),
    (-100, 60, 'Amérique\ndu Nord')
]

# Marquage des zones sur la carte
for lon, lat, label in zones_exemple:
    # Point noir pour marquer la position
    ax1.plot(lon, lat, 'ko', markersize=8, transform=ccrs.PlateCarree(), zorder=5)
    # Label avec fond jaune pour meilleure lisibilité
    ax1.text(lon, lat-8, label, transform=ccrs.PlateCarree(),
            fontsize=9, ha='center', fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='yellow', alpha=0.7))

# ==============================================================================
# CARTE 2 : PROJECTION ROBINSON (PSEUDO-CYLINDRIQUE)
# ==============================================================================
# Projection Robinson = compromis optimal pour représentations globales
# Utilisée par National Geographic, préserve mieux les surfaces et formes
ax2 = axes[1]
ax2.set_title('Projection Robinson (Pseudo-Cylindrique)\n' +
              '✓ Compromis optimal - Préserve mieux les surfaces et formes',
              fontsize=13, fontweight='bold', pad=15, color='darkgreen')

# Ajout des mêmes couches géographiques pour comparaison directe
ax2.add_feature(cfeature.LAND, facecolor='lightgray', edgecolor='black', linewidth=0.3)
ax2.add_feature(cfeature.OCEAN, facecolor='#e6f2ff')
ax2.add_feature(cfeature.COASTLINE, linewidth=0.5, edgecolor='black')
ax2.add_feature(cfeature.BORDERS, linewidth=0.3, edgecolor='gray', alpha=0.5)

# Visualisation des mêmes données de température
# Utilisation de transform=ccrs.PlateCarree() car les données sont en lat/lon
im2 = ax2.contourf(lon_grid, lat_grid, temp_anomaly,
                   levels=15, cmap='RdYlBu_r',
                   transform=ccrs.PlateCarree(),
                   alpha=0.75, vmin=0, vmax=5)

# Grille sans labels (Robinson gère mal les labels de grille)
ax2.gridlines(linewidth=0.5, color='gray', alpha=0.5, linestyle='--')

# Marquage des mêmes zones pour permettre la comparaison
for lon, lat, label in zones_exemple:
    ax2.plot(lon, lat, 'ko', markersize=8, transform=ccrs.PlateCarree(), zorder=5)
    ax2.text(lon, lat-8, label, transform=ccrs.PlateCarree(),
            fontsize=9, ha='center', fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='yellow', alpha=0.7))

# ==============================================================================
# LÉGENDE ET EXPORT
# ==============================================================================
# Colorbar commune aux deux cartes (utilise im2 mais s'applique aux deux axes)
cbar = fig.colorbar(im2, ax=axes, orientation='horizontal',
                    pad=0.05, shrink=0.6, aspect=30)
cbar.set_label('Anomalie de température moyenne (°C) - Scénario SSP5-8.5',
               fontsize=12, fontweight='bold')

# Ajustement automatique des espacements
plt.tight_layout()

# Export haute résolution pour rapports et présentations
plt.savefig('comparaison_projections.png', dpi=300, bbox_inches='tight')

# Affichage
plt.show()

# ==============================================================================
# MESSAGES DE SORTIE
# ==============================================================================
print("=" * 70)
print("✓ Visualisation générée avec succès")
print("=" * 70)
print("\n📊 POINTS CLÉS À RETENIR :")
print("  • PlateCarree : Simple mais déforme les surfaces aux hautes latitudes")
print("  • Robinson : Meilleur compromis pour les analyses globales")
print("  • Le choix de la projection impacte l'interprétation des données !")
print("\n🌍 Utilisé pour : ERA5-Land, WorldClim, CHIRPS, MSWEP")
print("=" * 70)