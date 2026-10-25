"""
Generate a clean college crest logo for Sri Eshwar College of Engineering (SECE)
resembling the official emblem from the template.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches

fig, ax = plt.subplots(figsize=(2.0, 2.5), dpi=300)
ax.axis('off')
ax.set_xlim(0, 10)
ax.set_ylim(0, 12.5)

# Shield outer shape
shield_x = [1, 9, 9, 5, 1]
shield_y = [11, 11, 4.5, 1, 4.5]
shield = patches.Polygon(list(zip(shield_x, shield_y)), closed=True, fc='#0D47A1', ec='#0D47A1', lw=2)
ax.add_patch(shield)

# Inner white shield
inner_x = [1.3, 8.7, 8.7, 5, 1.3]
inner_y = [10.7, 10.7, 4.7, 1.5, 4.7]
inner_shield = patches.Polygon(list(zip(inner_x, inner_y)), closed=True, fc='#FFFFFF', ec='#0D47A1', lw=1.5)
ax.add_patch(inner_shield)

# Center divider line
ax.plot([5, 5], [1.5, 10.7], color='#0D47A1', lw=1.5)
ax.plot([1.3, 8.7], [7.7, 7.7], color='#0D47A1', lw=1.5)

# Quadrant 1 (Top Left): Open Book
ax.plot([2.0, 3.2, 4.4], [9.3, 9.0, 9.3], color='#0D47A1', lw=2)
ax.plot([2.0, 3.2, 4.4], [8.6, 8.3, 8.6], color='#0D47A1', lw=2)
ax.plot([3.2, 3.2], [8.3, 9.0], color='#0D47A1', lw=2)

# Quadrant 2 (Top Right): Torch with flame
torch = patches.Rectangle((6.7, 8.0), 0.6, 1.2, fc='#0D47A1')
ax.add_patch(torch)
flame_x = [7.0, 7.4, 7.3, 7.0, 6.7, 6.6]
flame_y = [10.2, 9.6, 9.2, 9.2, 9.2, 9.6]
flame = patches.Polygon(list(zip(flame_x, flame_y)), closed=True, fc='#FF9800', ec='#E65100', lw=1)
ax.add_patch(flame)

# Quadrant 3 (Bottom Left): Star / Excellence
ax.text(3.1, 5.8, "★", fontsize=16, color='#0D47A1', ha='center', va='center')

# Quadrant 4 (Bottom Right): Pillar / Tower
pillar = patches.Rectangle((6.5, 4.0), 0.8, 3.2, fc='#0D47A1')
ax.add_patch(pillar)

# Top Ribbon: "Leadership & Excellence"
ribbon = patches.Rectangle((0.5, 11.2), 9, 1.1, fc='#1565C0', ec='#0D47A1', lw=1)
ax.add_patch(ribbon)
ax.text(5.0, 11.75, "Leadership & Excellence", color='white', fontsize=6.5, fontweight='bold', ha='center', va='center')

plt.tight_layout()
plt.savefig('figures/sece_logo.png', dpi=300, bbox_inches='tight', transparent=True)
plt.close()
print("College crest saved to figures/sece_logo.png")
