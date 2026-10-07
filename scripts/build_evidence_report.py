"""Generate Markdown/web/PDF reports from the dashboard's checked manifest.

Optional PDF dependency: pip install -r scripts/requirements.txt
"""
import html
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / 'web/public/evidence'


def main():
    data = json.loads((PUBLIC / 'bangladesh.json').read_text())
    sources = {s['id']: s for s in data['sources']}
    lines = ['# Bangladesh Mobile Financial Services Fraud & APP Scam Evidence Report',
             '', f"Checked public-source snapshot: {data['reviewed_at']}. This is not live data.", '',
             '## Executive summary', '',
             'Thamun targets manipulated customer-authorized payments before final authorization. Public ecosystem statistics establish scale; case reports and consumer-protection coverage establish related risks. They do not establish Thamun effectiveness or national APP prevalence.', '',
             '## Evidence limitations and research gap', '', data['notes']['evidence'], '', data['notes']['ml'], '', data['notes']['coverage'], '',
             'The named December 2025 Payment Systems Report could not be fetched; no PDF statistics or page numbers were guessed. Official statistics below come from a separately verified Bangladesh Bank web table. Police national fraud figures were not verified. Article publication dates are not assumed to be exact incident dates.', '',
             '## Bangladesh MFS ecosystem, fraud context and case studies', '']
    for item in data['items']:
        source = sources[item['source_id']]
        lines += [f"### {item['title']}", '', item['claim'], '',
                  f"- Category: {item['category']}; relevance: {item['relevance']}.",
                  f"- Source: {source['organization']} — {source['title']} (Tier {source['tier']}).",
                  f"- Publication date: {source.get('date') or 'Not supplied'}; observation/reporting date: {item['date']}.",
                  f"- Checked: {source['checked_at']}; locator: {source.get('locator', 'Article body')}.",
                  f"- URL: {source['url']}",
                  f"- Supports: {item['supports']}", f"- Does not establish: {item['limitations']}",
                  f"- Thamun connection: {item['feature']} (design rationale, not measured prevention).", '']
    scale = next(i for i in data['items'] if i['id'] == 'scale')
    a, b = scale['comparison']
    change = (b['value_crore_bdt'] - a['value_crore_bdt']) / a['value_crore_bdt'] * 100
    lines += ['## Statistical analysis', '',
              f"Monthly transaction value change, January–February 2025: ({b['value_crore_bdt']} − {a['value_crore_bdt']}) / {a['value_crore_bdt']} × 100 = {change:.2f}%.", '',
              'Source: Bangladesh Bank MFS web table, rows 7–8. Unequal month lengths affect totals. Two observations do not establish a long-term trend. No national fraud percentage, incident-loss sum, or money-saved estimate is calculated.', '',
              'The dashboard case count includes only items explicitly flagged as MFS incident case studies. Source-tier counts include only verified source records, not inaccessible URLs or independent corroborations. Registered/active accounts are not interchangeable with unique people.', '',
              '## Source quality and verification gaps', '',
              'Tier 1: official; Tier 2: institutional/research; Tier 3: established media. PRI is an institutional host of media coverage, not a freshly inspected microdataset. BSS attribution is syndicated reporting at TBS, not an independently verified BSS page. Media allegations remain attributed allegations.', '']
    for source in data['sources']:
        lines += [f"### {source['organization']}: {source['title']}", '',
                  f"Status: {source['status']}. Tier {source['tier']}. Published: {source.get('date') or 'Not supplied'}. Checked: {source['checked_at']}.", '',
                  source.get('note', 'Source article text checked; no independent investigation performed.'), '', source['url'], '']
        if source.get('retrieval_url'):
            lines += [f"Publisher mirror used for verification: {source['retrieval_url']}", '']
    lines += ['## Why Thamun is relevant', '',
              'Pre-authorization explanation and purpose inquiry provide a place to reconsider manipulated payments. Recipient history and appropriately qualified reports add context. Adaptive intervention aims to limit unnecessary disruption; that benefit requires evaluation. Coaching can support understanding without shaming the customer.', '',
              'The simulated prototype does not integrate with live wallets or prevent OTP theft outside its payment flow. Real customer evaluation, provider integration, representative APP labels and deployment/legal review remain necessary.', '',
              '## Reproduction', '',
              'The single source manifest is `web/public/evidence/bangladesh.json`. Run `python scripts/build_evidence_report.py` to regenerate this report and its public copies. Reverify source content before updating facts; do not scrape at runtime or present this dated snapshot as current data.', '']
    text = '\n'.join(lines)
    (ROOT / 'docs/bangladesh_mfs_evidence_report.md').write_text(text, encoding='utf-8')
    (PUBLIC / 'report.md').write_text(text, encoding='utf-8')
    try:
        from reportlab.lib import colors
        from reportlab.lib.enums import TA_LEFT
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.pagesizes import A4
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont
    except ImportError:
        print('Markdown report generated. Install scripts/requirements.txt for PDF generation.')
        return
    font_path = Path('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')
    font_name = 'Helvetica'
    if font_path.exists():
        pdfmetrics.registerFont(TTFont('EvidenceSans', str(font_path)))
        font_name = 'EvidenceSans'
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='BodyEvidence', fontName=font_name, fontSize=9, leading=14,
                              textColor=colors.HexColor('#21383d'), spaceAfter=7, splitLongWords=True))
    styles.add(ParagraphStyle(name='TitleEvidence', fontName=font_name, fontSize=21, leading=27,
                              textColor=colors.HexColor('#0f4c5c'), spaceAfter=18))
    styles.add(ParagraphStyle(name='H2Evidence', fontName=font_name, fontSize=14, leading=19, spaceBefore=16,
                              spaceAfter=8, textColor=colors.HexColor('#0f4c5c'), keepWithNext=True))
    styles.add(ParagraphStyle(name='H3Evidence', fontName=font_name, fontSize=11, leading=16, spaceBefore=12,
                              spaceAfter=6, keepWithNext=True))
    story = []
    for line in lines:
        if not line:
            continue
        if line.startswith('# '):
            style, line = 'TitleEvidence', line[2:]
        elif line.startswith('## '):
            style, line = 'H2Evidence', line[3:]
        elif line.startswith('### '):
            style, line = 'H3Evidence', line[4:]
        else:
            style = 'BodyEvidence'
        story.append(Paragraph(html.escape(line).replace('—', '-').replace('–', '-'), styles[style]))
    def footer(canvas, doc):
        canvas.saveState()
        canvas.setFont(font_name, 8)
        canvas.setFillColor(colors.HexColor('#5e7075'))
        canvas.drawString(42, 25, 'Thamun | Public evidence snapshot | 7 October 2026')
        canvas.drawRightString(A4[0]-42, 25, str(doc.page))
        canvas.restoreState()
    path = ROOT / 'docs/bangladesh_mfs_evidence_report.pdf'
    SimpleDocTemplate(str(path), pagesize=A4, rightMargin=42, leftMargin=42, topMargin=42, bottomMargin=45,
                      title='Bangladesh MFS Fraud & APP Evidence', author='Thamun project').build(story, onFirstPage=footer, onLaterPages=footer)
    shutil.copyfile(path, PUBLIC / 'report.pdf')
    print(f'Generated Markdown and PDF evidence reports: {path.name}')


if __name__ == '__main__':
    main()
