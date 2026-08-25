from flask import Flask, render_template, jsonify, request
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_root))

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64
import json
from contextlib import redirect_stdout

# Import configuration system
from config import ExperimentConfig

# Import all experiments
from experiments.noise_sweep import run_noise_sweep
from experiments.monte_carlo import run_monte_carlo
from experiments.attack_analysis import run_attack_analysis
from experiments.security_deep_dive import run_security_deep_dive
from experiments.error_correction_demo import run_error_correction_demo
from experiments.decoy_state_demo import run_decoy_state_demo
from experiments.privacy_amplification_demo import run_privacy_amplification_demo
from experiments.secure_communication_demo import run_secure_communication_demo
from experiments.advanced_attack_demo import run_advanced_attack_analysis
from experiments.randomness_analysis import run_randomness_analysis
from experiments.statistical_analysis import run_statistical_analysis

app = Flask(__name__, template_folder='templates', static_folder='static')

# Experiment configurations
EXPERIMENTS = {
    "1": {
        "name": "Noise Sweep Analysis",
        "description": "Analyzes QBER vs noise probability",
        "category": "Basic Experiments",
        "color": "#FF6B6B",
        "func": run_noise_sweep,
        "icon": "📊"
    },
    "2": {
        "name": "Monte Carlo Simulation",
        "description": "Statistical distribution of 200 protocol runs",
        "category": "Basic Experiments",
        "color": "#4ECDC4",
        "func": run_monte_carlo,
        "icon": "🎲"
    },
    "3": {
        "name": "Attack Analysis",
        "description": "Compare QBER under different eavesdropping attacks",
        "category": "Basic Experiments",
        "color": "#95E1D3",
        "func": run_attack_analysis,
        "icon": "🛡️"
    },
    "4": {
        "name": "Security Deep Dive",
        "description": "Information theory & security analysis with SecurityAnalyzer",
        "category": "Core Systems Analysis",
        "color": "#F38181",
        "func": run_security_deep_dive,
        "icon": "🔐"
    },
    "5": {
        "name": "Error Correction Demo",
        "description": "Error correction performance and information leakage",
        "category": "Core Systems Analysis",
        "color": "#AA96DA",
        "func": run_error_correction_demo,
        "icon": "🔧"
    },
    "6": {
        "name": "Decoy State Analysis",
        "description": "Decoy-state mechanism for enhanced security detection",
        "category": "Core Systems Analysis",
        "color": "#FCBAD3",
        "func": run_decoy_state_demo,
        "icon": "🎭"
    },
    "7": {
        "name": "Privacy Amplification Demo",
        "description": "Key compression using universal hashing",
        "category": "Core Systems Analysis",
        "color": "#A8DADC",
        "func": run_privacy_amplification_demo,
        "icon": "🔒"
    },
    "8": {
        "name": "Secure Communication Demo",
        "description": "AES encryption using QKD-derived keys",
        "category": "Advanced Features",
        "color": "#FFB4A2",
        "func": run_secure_communication_demo,
        "icon": "💬"
    },
    "9": {
        "name": "Advanced Attack Analysis",
        "description": "Deep dive into AttackEngine with 3 strategies",
        "category": "Advanced Features",
        "color": "#E0AAFF",
        "func": run_advanced_attack_analysis,
        "icon": "⚔️"
    },
    "10": {
        "name": "Randomness Quality Analysis",
        "description": "RandomnessManager testing and entropy analysis",
        "category": "Advanced Features",
        "color": "#C1B1FF",
        "func": run_randomness_analysis,
        "icon": "🎰"
    },
    "11": {
        "name": "Statistical Analysis",
        "description": "Comprehensive protocol statistical validation",
        "category": "Advanced Features",
        "color": "#FFD6A5",
        "func": run_statistical_analysis,
        "icon": "📈"
    }
}

@app.route('/')
def index():
    """Main page with experiment cards"""
    return render_template('index.html', experiments=EXPERIMENTS)

@app.route('/api/experiments')
def get_experiments():
    """API endpoint to get all experiments"""
    return jsonify(EXPERIMENTS)

@app.route('/api/run/<exp_id>', methods=['POST'])
def run_experiment(exp_id):
    """Run a specific experiment and return results"""
    if exp_id not in EXPERIMENTS:
        return jsonify({"error": "Experiment not found"}), 404
    
    try:
        exp = EXPERIMENTS[exp_id]
        
        # Capture output
        output = io.StringIO()
        with redirect_stdout(output):
            exp["func"]()
        
        console_output = output.getvalue()
        
        return jsonify({
            "success": True,
            "name": exp["name"],
            "output": console_output,
            "color": exp["color"]
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "type": type(e).__name__
        }), 500

@app.route('/api/experiment/<exp_id>')
def get_experiment_info(exp_id):
    """Get information about a specific experiment"""
    if exp_id not in EXPERIMENTS:
        return jsonify({"error": "Experiment not found"}), 404
    
    exp = EXPERIMENTS[exp_id]
    return jsonify({
        "id": exp_id,
        "name": exp["name"],
        "description": exp["description"],
        "category": exp["category"],
        "color": exp["color"],
        "icon": exp["icon"]
    })

# ============================================================================
# CONFIGURATION API ENDPOINTS
# ============================================================================

@app.route('/api/config/current', methods=['GET'])
def get_current_config():
    """Get current configuration"""
    return jsonify({
        "quantum": {
            "num_qubits": ExperimentConfig.NUM_QUBITS,
            "num_bases": ExperimentConfig.NUM_BASES
        },
        "noise": {
            "min_noise": ExperimentConfig.MIN_NOISE,
            "max_noise": ExperimentConfig.MAX_NOISE,
            "noise_levels": ExperimentConfig.NOISE_LEVELS
        },
        "simulation": {
            "monte_carlo_runs": ExperimentConfig.MONTE_CARLO_RUNS,
            "statistical_runs": ExperimentConfig.STATISTICAL_RUNS
        },
        "security": {
            "qber_threshold": ExperimentConfig.QBER_THRESHOLD,
            "honest_qber": ExperimentConfig.HONEST_QBER,
            "information_leakage_tolerance": ExperimentConfig.INFORMATION_LEAKAGE_TOLERANCE
        },
        "privacy": {
            "amplification_method": ExperimentConfig.PRIVACY_AMPLIFICATION_METHOD,
            "compression_ratio": ExperimentConfig.PRIVACY_COMPRESSION_RATIO
        },
        "attacks": {
            "enable_pns_attack": ExperimentConfig.ENABLE_PNS_ATTACK,
            "enable_intercept_resend": ExperimentConfig.ENABLE_INTERCEPT_RESEND,
            "enable_trojan_horse": ExperimentConfig.ENABLE_TROJAN_HORSE
        },
        "output": {
            "verbose": ExperimentConfig.VERBOSE_OUTPUT,
            "show_statistics": ExperimentConfig.SHOW_STATISTICS
        }
    })

@app.route('/api/config/preset/<preset_name>', methods=['POST'])
def apply_preset(preset_name):
    """Apply a configuration preset"""
    try:
        if preset_name == "fast":
            ExperimentConfig.preset_fast()
            name = "Fast & Simple"
        elif preset_name == "balanced":
            ExperimentConfig.preset_balanced()
            name = "Balanced"
        elif preset_name == "detailed":
            ExperimentConfig.preset_detailed()
            name = "Detailed"
        elif preset_name == "comprehensive":
            ExperimentConfig.preset_comprehensive()
            name = "Comprehensive"
        else:
            return jsonify({"error": "Unknown preset"}), 400
        
        return jsonify({
            "success": True,
            "message": f"Applied {name} preset",
            "config": {
                "qubits": ExperimentConfig.NUM_QUBITS,
                "noise_levels": ExperimentConfig.NOISE_LEVELS,
                "mc_runs": ExperimentConfig.MONTE_CARLO_RUNS,
                "stat_runs": ExperimentConfig.STATISTICAL_RUNS
            }
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/config/update', methods=['POST'])
def update_config():
    """Update configuration from JSON"""
    try:
        data = request.json
        
        # Update quantum settings
        if 'quantum' in data:
            if 'num_qubits' in data['quantum']:
                ExperimentConfig.NUM_QUBITS = int(data['quantum']['num_qubits'])
        
        # Update noise settings
        if 'noise' in data:
            if 'min_noise' in data['noise']:
                ExperimentConfig.MIN_NOISE = float(data['noise']['min_noise'])
            if 'max_noise' in data['noise']:
                ExperimentConfig.MAX_NOISE = float(data['noise']['max_noise'])
            if 'noise_levels' in data['noise']:
                ExperimentConfig.NOISE_LEVELS = int(data['noise']['noise_levels'])
        
        # Update simulation settings
        if 'simulation' in data:
            if 'monte_carlo_runs' in data['simulation']:
                ExperimentConfig.MONTE_CARLO_RUNS = int(data['simulation']['monte_carlo_runs'])
            if 'statistical_runs' in data['simulation']:
                ExperimentConfig.STATISTICAL_RUNS = int(data['simulation']['statistical_runs'])
        
        # Update security settings
        if 'security' in data:
            if 'qber_threshold' in data['security']:
                ExperimentConfig.QBER_THRESHOLD = float(data['security']['qber_threshold'])
        
        # Update privacy settings
        if 'privacy' in data:
            if 'amplification_method' in data['privacy']:
                ExperimentConfig.PRIVACY_AMPLIFICATION_METHOD = data['privacy']['amplification_method']
            if 'compression_ratio' in data['privacy']:
                ExperimentConfig.PRIVACY_COMPRESSION_RATIO = float(data['privacy']['compression_ratio'])
        
        # Update attacks
        if 'attacks' in data:
            if 'enable_pns_attack' in data['attacks']:
                ExperimentConfig.ENABLE_PNS_ATTACK = bool(data['attacks']['enable_pns_attack'])
            if 'enable_intercept_resend' in data['attacks']:
                ExperimentConfig.ENABLE_INTERCEPT_RESEND = bool(data['attacks']['enable_intercept_resend'])
            if 'enable_trojan_horse' in data['attacks']:
                ExperimentConfig.ENABLE_TROJAN_HORSE = bool(data['attacks']['enable_trojan_horse'])
        
        # Update output settings
        if 'output' in data:
            if 'verbose' in data['output']:
                ExperimentConfig.VERBOSE_OUTPUT = bool(data['output']['verbose'])
            if 'show_statistics' in data['output']:
                ExperimentConfig.SHOW_STATISTICS = bool(data['output']['show_statistics'])
        
        return jsonify({
            "success": True,
            "message": "Configuration updated successfully"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/config/save', methods=['POST'])
def save_config():
    """Save configuration to file"""
    try:
        data = request.json
        filename = data.get('filename', 'config.json')
        
        # Ensure .json extension
        if not filename.endswith('.json'):
            filename += '.json'
        
        # Remove any path separators for security
        filename = filename.replace('/', '_').replace('\\', '_')
        
        # Save in web folder
        filepath = Path(__file__).parent / 'configs' / filename
        filepath.parent.mkdir(exist_ok=True)
        
        ExperimentConfig.save_config(str(filepath))
        
        return jsonify({
            "success": True,
            "message": f"Configuration saved to {filename}",
            "filename": filename
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/config/load', methods=['POST'])
def load_config_endpoint():
    """Load configuration from file"""
    try:
        data = request.json
        filename = data.get('filename', 'config.json')
        
        # Ensure .json extension
        if not filename.endswith('.json'):
            filename += '.json'
        
        # Remove any path separators for security
        filename = filename.replace('/', '_').replace('\\', '_')
        
        # Load from web folder
        filepath = Path(__file__).parent / 'configs' / filename
        
        if not filepath.exists():
            return jsonify({"error": f"Configuration file not found: {filename}"}), 404
        
        ExperimentConfig.load_config(str(filepath))
        
        return jsonify({
            "success": True,
            "message": f"Configuration loaded from {filename}",
            "config": {
                "qubits": ExperimentConfig.NUM_QUBITS,
                "noise_levels": ExperimentConfig.NOISE_LEVELS,
                "mc_runs": ExperimentConfig.MONTE_CARLO_RUNS
            }
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/config/presets', methods=['GET'])
def get_presets():
    """Get available presets"""
    return jsonify({
        "presets": [
            {
                "id": "fast",
                "name": "Fast & Simple",
                "description": "4 qubits, 5 noise levels, 50 runs - Quick demo",
                "time": "5-10 seconds"
            },
            {
                "id": "balanced",
                "name": "Balanced",
                "description": "8 qubits, 10 noise levels, 200 runs - Standard analysis",
                "time": "30-45 seconds"
            },
            {
                "id": "detailed",
                "name": "Detailed",
                "description": "8 qubits, 20 noise levels, 200 runs - Good statistics",
                "time": "1-2 minutes"
            },
            {
                "id": "comprehensive",
                "name": "Comprehensive",
                "description": "12 qubits, 15 noise levels, 300 runs - Research grade",
                "time": "3-5 minutes"
            }
        ]
    })

@app.route('/api/config/list', methods=['GET'])
def list_saved_configs():
    """List all saved configuration files"""
    try:
        configs_dir = Path(__file__).parent / 'configs'
        configs = []
        
        if configs_dir.exists():
            for config_file in configs_dir.glob('*.json'):
                configs.append({
                    "filename": config_file.name,
                    "name": config_file.stem
                })
        
        return jsonify({
            "success": True,
            "configs": sorted(configs, key=lambda x: x['filename'])
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/config/delete/<config_name>', methods=['DELETE'])
def delete_config(config_name):
    """Delete a saved configuration file"""
    try:
        # Ensure .json extension
        if not config_name.endswith('.json'):
            config_name += '.json'
        
        # Remove any path separators for security
        config_name = config_name.replace('/', '_').replace('\\', '_')
        
        # Delete from web folder
        filepath = Path(__file__).parent / 'configs' / config_name
        
        if not filepath.exists():
            return jsonify({"error": f"Configuration file not found: {config_name}"}), 404
        
        filepath.unlink()
        
        return jsonify({
            "success": True,
            "message": f"Configuration deleted: {config_name}"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/about')
def about():
    """About page"""
    return render_template('about.html')

@app.route('/documentation')
def documentation():
    """Documentation page"""
    return render_template('documentation.html', experiments=EXPERIMENTS)

@app.route('/configuration')
def configuration():
    """Configuration page"""
    return render_template('configuration.html')

@app.route('/results')
def results():
    """Results and status page"""
    return render_template('results.html')

if __name__ == '__main__':
    print("\n" + "="*70)
    print("BB84 ADAPTIVE QKD - WEB INTERFACE")
    print("="*70)
    print("\n[*] Starting web server...")
    print("[*] Open your browser and go to: http://localhost:5000")
    print("\n[*] Available Pages:")
    print("   - Home:          http://localhost:5000/")
    print("   - Configuration: http://localhost:5000/configuration")
    print("   - Results:       http://localhost:5000/results")
    print("   - About:         http://localhost:5000/about")
    print("   - Documentation: http://localhost:5000/documentation")
    print("\n[*] Current Configuration:")
    print(f"   - Qubits: {ExperimentConfig.NUM_QUBITS}")
    print(f"   - Noise: {ExperimentConfig.MIN_NOISE*100:.1f}% - {ExperimentConfig.MAX_NOISE*100:.1f}% ({ExperimentConfig.NOISE_LEVELS} levels)")
    print(f"   - MC Runs: {ExperimentConfig.MONTE_CARLO_RUNS}")
    print(f"   - Statistical Runs: {ExperimentConfig.STATISTICAL_RUNS}")
    print(f"   - QBER Threshold: {ExperimentConfig.QBER_THRESHOLD*100:.1f}%")
    print("\n[*] Press Ctrl+C to stop the server\n")
    app.run(debug=True, port=5000, use_reloader=False)
