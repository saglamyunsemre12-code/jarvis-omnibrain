#!/usr/bin/env python3
"""
JARVIS Higgsfield & Remotion Engine — Cinematic Video & Motion Graphics Studio
Generates optimized Higgsfield AI prompts (Camera movements, Lighting, Cinema Studio, 9:16 vertical)
and builds React Remotion code for animated typography and graphics.
"""

import json

def generate_higgsfield_prompt(concept, style="cinematic_luxury", ratio="9:16"):
    """
    Constructs high-conversion, professional cinematic prompt syntax tailored for Higgsfield AI models
    (Genjutsu / Cinema Studio / Ads Studio).
    """
    lighting_presets = {
        "cinematic_luxury": "Warm ambient golden hour rim lighting, soft volumetric haze, Forbes 5-star resort aesthetic, shot on ARRI Alexa 35, 85mm anamorphic lens, shallow depth of field, photorealistic, 8k resolution, elegant color grading.",
        "cyberpunk_tech": "Neon cyan and deep onyx shadows, high contrast, holographic volumetric displays, Blade Runner 2049 aesthetic, anamorphic lens flare, sharp 8k textures.",
        "minimalist_clean": "Bright architectural studio lighting, neutral tones, Scandinavian luxury minimalism, clean glass reflections, ultra-crisp 4k."
    }

    camera_moves = [
        "Smooth slow push-in tracking shot, stabilizing gimbal movement",
        "Low-angle upward dolly shot with subtle tilt",
        "Orbital 360-degree floating camera with focus transition"
    ]

    selected_lighting = lighting_presets.get(style, lighting_presets["cinematic_luxury"])
    camera_move = camera_moves[0]

    prompt_package = {
        "concept": concept,
        "aspect_ratio": ratio,
        "style_preset": style,
        "higgsfield_prompt": f"Cinematic film still: {concept}. {camera_move}. {selected_lighting} No distortion, hyper-detailed textures, masterwork cinematography.",
        "negative_prompt": "cartoon, oversaturated, blurry, bad anatomy, lowres, text watermark, flicker, jitter, amateur footage",
        "parameters": {
            "fps": 30,
            "motion_bucket": 127,
            "guidance_scale": 7.5,
            "steps": 40
        }
    }
    return prompt_package

def generate_remotion_component(title, subtitle, duration_sec=5):
    """
    Generates a drop-in React Remotion component code with spring animations and typography.
    """
    frames = duration_sec * 30
    code = f"""import {{ interpolate, spring, useCurrentFrame, useVideoConfig }} from 'remotion';

export const LuxuryTitleCard = () => {{
  const frame = useCurrentFrame();
  const {{ fps }} = useVideoConfig();

  const titleProgress = spring({{ frame, fps, config: {{ damping: 12, mass: 0.5 }} }});
  const subtitleOpacity = interpolate(frame, [15, 30], [0, 1], {{ extrapolateRight: 'clamp' }});

  return (
    <div style={{{{
      flex: 1,
      backgroundColor: '#090a0f',
      display: 'flex',
      flexDirection: 'column',
      justifyContent: 'center',
      alignItems: 'center',
      fontFamily: 'sans-serif'
    }}}}>
      <h1 style={{{{
        color: '#e6ca85',
        fontSize: '64px',
        fontWeight: 'bold',
        transform: `scale(${{titleProgress}})`,
        margin: 0,
        textShadow: '0 0 20px rgba(230,202,133,0.3)'
      }}}}>
        {title}
      </h1>
      <p style={{{{
        color: '#9ca3af',
        fontSize: '28px',
        opacity: subtitleOpacity,
        marginTop: '16px',
        letterSpacing: '0.1em',
        textTransform: 'uppercase'
      }}}}>
        {subtitle}
      </p>
    </div>
  );
}};
// Total duration: {frames} frames ({duration_sec}s @ 30fps)
"""
    return code

if __name__ == "__main__":
    p = generate_higgsfield_prompt("Luxury suite morning coffee service with panoramic sea view in Bodrum")
    print("Higgsfield Prompt Package:\n", json.dumps(p, indent=2))
