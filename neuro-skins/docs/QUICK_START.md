# NeuroSkins Quick Start Guide

## Installation

```bash
cd neuro-skins
pip install -r requirements.txt
```

## Basic Usage

### Command Line

Start a 20-minute Lite tier session:
```bash
python main.py --tier lite --duration 20 --age 25 --simulation
```

Start a Pro tier session:
```bash
python main.py --tier pro --duration 30 --age 30 --simulation
```

### API Server

Start the API server:
```bash
python -m src.api.server
```

Access API docs: http://localhost:8000/docs

### Web Dashboard

1. Start the API server (see above)
2. Open `src/ui/dashboard.html` in your browser
3. Configure settings and click "Start Session"

## Product Tiers

### Lite ($299)
- Basic 40 Hz gamma boost
- Trauma pattern deletion
- Morning fog protocol
- 3 transducers (crown, mastoids)

### Pro ($899)
- Full protocol suite
- HRV monitoring
- Cortisol tracking
- Anxiety/stress protocols
- 5 transducers
- Workout optimization

### Ascend ($2,499)
- Everything in Pro
- Kali/Shiva sex synchronization
- Ego death protocol (Day 23+)
- Float tank integration
- 7 transducers + pubic clip
- Partner sync capability

## Available Protocols

### Lite Tier
- **40 Hz Gamma Boost**: Peak cognitive performance (20 min)
- **Trauma Pattern Deletion**: Disrupts maladaptive patterns (15 min)

### Pro Tier (includes Lite)
- **Vagus Nerve Overclock**: Parasympathetic activation (10 min)
- **Anxiety Relief**: Rapid anxiety reduction (15 min)
- **Workout Prime**: Pre-workout optimization (10 min)
- **Berberine Alert**: Metabolic optimization (15 min)

### Ascend Tier (includes all)
- **Kali/Shiva Sync**: Tantric energy synchronization (30 min, 18+)
- **Layer 7 Ego Death**: Deep ego dissolution (45 min, 21+, Day 23+)
- **Float Tank Lock**: Sensory deprivation optimization (60 min)

## Safety Features

- Heart rate monitoring (abort >185 bpm)
- 90-minute gamma protocol limit
- Age restrictions enforced
- On-device data encryption
- Emergency stop capability

## API Examples

### Start Session
```bash
curl -X POST http://localhost:8000/session/start \
  -H "Content-Type: application/json" \
  -d '{
    "tier": "lite",
    "user_id": "user123",
    "age": 25,
    "duration_minutes": 20,
    "simulation": true
  }'
```

### Get Status
```bash
curl http://localhost:8000/status
```

### Stop Session
```bash
curl -X POST http://localhost:8000/session/stop
```

### List Protocols
```bash
curl http://localhost:8000/protocols?tier=pro
```

## Testing

Run tests:
```bash
cd tests
pytest test_system.py -v
```

## Troubleshooting

**Hardware not connecting:**
- Check Bluetooth is enabled
- Ensure transducers are charged
- Restart the system

**Low safety score:**
- Check sensor contact quality
- Reduce session intensity
- Take a break

**Protocol not activating:**
- Verify tier access
- Check age restrictions
- Ensure hardware is initialized

## Next Steps

1. Read the full documentation in `docs/`
2. Explore the API at http://localhost:8000/docs
3. Customize protocols in `src/protocols/library.py`
4. Train custom AI models for better classification

## Support

For issues or questions, check the documentation or file a GitHub issue.
