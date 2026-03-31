import pandas as pd

# Cargar datos
battles = pd.read_csv('archive/battles.csv')
battle_actors = pd.read_csv('archive/battle_actors.csv')

# Limpieza rápida de columnas numéricas
for c in ['wina', 'front', 'depth', 'kmda', 'crit', 'resa']:
    if c in battles.columns:
        battles[c] = pd.to_numeric(battles[c], errors='coerce')

# 1) Estadísticas generales
num_battles = len(battles)
num_wars = battles['war'].nunique()
num_locations = battles['locn'].nunique()

# 2) Guerras con más batallas
top_wars = battles['war'].value_counts().head(10)

# 3) Tipos de victorias (wina)
if 'wina' in battles.columns:
    win_distribution = battles['wina'].value_counts(dropna=False)
else:
    win_distribution = None

# 4) Terrenos más comunes
terrain_stats = battles['terra'].fillna('Unknown').value_counts().head(10)

# 5) Actores más frecuentes
actors_stats = battle_actors['actor'].value_counts().head(10)

# 6) Composición de fuerzas por guerra (participantes)
participation = (
    battle_actors.groupby('war')['actor']
    .nunique()
    .sort_values(ascending=False)
    .head(10)
)

# 7) Batallas con mayor número de actores
actors_per_battle = (
    battle_actors.groupby('isqno')['actor']
    .nunique()
    .sort_values(ascending=False)
    .head(10)
)

print('=== Resumen de investigación (archive) ===')
print(f'Total de batallas: {num_battles}')
print(f'Total de guerras: {num_wars}')
print(f'Total de ubicaciones únicas: {num_locations}')
print('\nTop 10 guerras por número de batallas:')
print(top_wars.to_string())
print('\nDistribución de wina (resultado):')
print(win_distribution.to_string() if win_distribution is not None else 'No disponible')
print('\nTop 10 terrenos:')
print(terrain_stats.to_string())
print('\nTop 10 actores en batallas:')
print(actors_stats.to_string())
print('\nTop 10 guerras por número de actores distintos:')
print(participation.to_string())
print('\nTop 10 batallas por cantidad de actores:')
print(actors_per_battle.to_string())

# 8) Opcional: batallas Epicenter con mayor front width
if 'front' in battles.columns:
    top_front = battles[['isqno', 'name', 'war', 'front']].sort_values('front', ascending=False).head(5)
    print('\nTop 5 batallas con mayor front (ancho frontal):')
    print(top_front.to_string(index=False))

# 9) Guardar un CSV de resumen rápido
summary = {
    'num_battles': [num_battles],
    'num_wars': [num_wars],
    'num_locations': [num_locations],
}
pd.DataFrame(summary).to_csv('analysis_archive_summary.csv', index=False)

print('\nInforme guardado en analysis_archive_summary.csv')
