
import json
from flask import Blueprint, jsonify, render_template, request
from app import db
from app.models import Scan
from app.scanner import scan_page
from app.recommendations import explain_violation
from app.code_analyzer import analyze_html

main = Blueprint('main', __name__)


@main.get('/')
def index():
    recent = Scan.query.order_by(Scan.created_at.desc()).limit(8).all()
    return render_template('index.html', recent=recent)


@main.get('/health')
def health():
    return jsonify(status='ok', application='AccessiAI')


@main.get('/api/history')
def api_history():
    records = Scan.query.order_by(Scan.created_at.desc()).limit(20).all()
    return jsonify(items=[{
        'id': item.id,
        'url': item.target_url,
        'score': item.score,
        'violation_count': item.violation_count,
        'created_at': item.created_at.isoformat(),
    } for item in records])


@main.post('/api/scan')
def api_scan():
    payload = request.get_json(silent=True) or {}
    target = (payload.get('url') or '').strip()

    if not target:
        return jsonify(error='Enter a webpage URL to scan.'), 400

    try:
        result = scan_page(target)
        total = sum(item['count'] for item in result['violations'])
        score = max(0, min(100, round(100 - total * 2)))

        enriched = [
            {**item, **explain_violation(item)}
            for item in result['violations']
        ]

        result.update({
            'violations': enriched,
            'violation_count': total,
            'score': score,
            'score_note': (
                'Illustrative indicator based on detected violation instances; '
                'not a WCAG conformance score.'
            ),
        })

        record = Scan(
            target_url=result['url'],
            score=score,
            violation_count=total,
            summary_json=json.dumps(enriched),
        )

        db.session.add(record)
        db.session.commit()

        return jsonify(result)

    except ValueError as exc:
        return jsonify(error=str(exc)), 400

    except RuntimeError as exc:
        return jsonify(error=str(exc)), 502

    except Exception:
        db.session.rollback()
        return jsonify(
            error='The scan could not be completed. Check the URL and try again.'
        ), 502


@main.post('/api/analyze-code')
def api_analyze_code():
    payload = request.get_json(silent=True) or {}
    source = payload.get('code', '')

    try:
        result = analyze_html(source)
        return jsonify(result)

    except ValueError as exc:
        return jsonify(error=str(exc)), 400

    except Exception:
        return jsonify(
            error='Code analysis failed. Please try again.'
        ), 500
