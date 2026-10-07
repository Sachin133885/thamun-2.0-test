import { useMemo, useState } from 'react'
import manifest from '../../public/evidence/bangladesh.json'
import '../evidence.css'

const QUALITY = { 1: 'Official', 2: 'Institutional / research', 3: 'Media reporting' }
const format = (n) => new Intl.NumberFormat('en-BD', { maximumFractionDigits: 2 }).format(n)

function SourceLink({ source }) {
  return <a href={source.url} target="_blank" rel="noopener noreferrer" className="ev-source-link">{source.organization} ↗</a>
}

function Quality({ source }) {
  return <span className={`ev-badge tier-${source.tier}`}>Tier {source.tier} · {QUALITY[source.tier]}</span>
}

export function EvidenceEntry({ onOpen, lang = 'en' }) {
  return <section className="ev-entry">
    <div className="ev-entry-label">PUBLIC EVIDENCE · BANGLADESH</div>
    <h3>🇧🇩 {lang === 'bn' ? 'বাংলাদেশের বাস্তব প্রমাণ' : 'Bangladesh Real Evidence'}</h3>
    <p>{lang === 'bn' ? 'প্রকাশ্য উৎস, ঘটনার বিবরণ ও উৎসের মান। মডেলের নমুনা ডেটা থেকে আলাদা।' : 'Verified public sources, incident cases and source quality. Separate from synthetic model results.'}</p>
    <button className="btn primary small" onClick={onOpen}>{lang === 'bn' ? 'প্রমাণের ড্যাশবোর্ড দেখুন →' : 'View Evidence Dashboard →'}</button>
    <small>Historical snapshot · checked {manifest.reviewed_at}</small>
  </section>
}

export default function Evidence({ onBack, lang = 'en', onLanguage }) {
  const [category, setCategory] = useState('All')
  const [tier, setTier] = useState('all')
  const [query, setQuery] = useState('')
  const [showReport, setShowReport] = useState(false)
  const [report, setReport] = useState(null)
  const [reportError, setReportError] = useState('')
  const sources = Object.fromEntries(manifest.sources.map((s) => [s.id, s]))
  const scale = manifest.items.find((i) => i.id === 'scale')
  const incidents = manifest.items.filter((i) => i.incident).sort((a, b) => a.date.localeCompare(b.date))
  const categories = ['All', ...new Set(manifest.items.map((i) => i.category))]
  const filtered = useMemo(() => manifest.items.filter((item) =>
    (category === 'All' || item.category === category) &&
    (tier === 'all' || sources[item.source_id].tier === Number(tier)) &&
    `${item.title} ${item.claim} ${sources[item.source_id].organization}`.toLowerCase().includes(query.toLowerCase())), [category, tier, query])
  const verified = manifest.sources.filter((s) => s.status === 'verified')
  const official = verified.filter((s) => s.tier === 1)
  const diff = (scale.comparison[1].value_crore_bdt - scale.comparison[0].value_crore_bdt) / scale.comparison[0].value_crore_bdt * 100

  const openReport = async () => {
    setShowReport(!showReport)
    if (report) return
    try {
      const response = await fetch('/evidence/report.md')
      if (!response.ok) throw new Error('The full report could not be loaded.')
      setReport(await response.text())
    } catch (e) { setReportError(e.message) }
  }

  return <main className="evidence-page" lang={lang}>
    <header className="ev-topbar">
      <a className="ev-brand" href="#demo" onClick={onBack}><span className="ev-mark">থ</span> Thamun <small>Pause. Understand. Decide.</small></a>
      <nav aria-label="Evidence navigation"><a href="#ev-sources">Sources</a><a href="#evaluation">AI / ML</a><button onClick={onLanguage}>{lang === 'en' ? 'বাংলা' : 'EN'}</button><button onClick={onBack}>← Payment demo</button></nav>
    </header>
    <div className="ev-container">
      <section className="ev-hero">
        <div><span className="ev-eyebrow">BANGLADESH · PUBLIC EVIDENCE</span>
          <h1>{lang === 'bn' ? 'বাংলাদেশের এমএফএস জালিয়াতি ও APP সম্পর্কিত প্রমাণ' : 'Bangladesh MFS Fraud & APP Evidence'}</h1>
          <p>{lang === 'bn' ? 'চূড়ান্ত অনুমোদনের আগে আর্থিক সুরক্ষার প্রয়োজন বোঝাতে যাচাই করা প্রকাশ্য তথ্য।' : 'What is happening in Bangladesh—and why a pause before final authorization matters.'}</p>
          <div className="ev-hero-badges"><span className="ev-badge">Evidence-based · publicly checked sources</span><span className="ev-badge">Historical snapshot · {manifest.reviewed_at}</span></div>
        </div><div className="ev-flag" aria-label="Bangladesh flag"><span /></div>
      </section>

      <div className="ev-disclaimer"><strong>Evidence note.</strong> {manifest.notes.evidence}<br /><strong>ML note.</strong> {manifest.notes.ml}</div>

      <section className="ev-stats" aria-label="Verified evidence overview">
        <article><span>MFS transaction value</span><strong>৳{format(scale.metrics.transaction_value_crore_bdt)}<small>crore BDT</small></strong><p>February 2025 · web table, row 8</p><SourceLink source={sources['bb-mfs']} /></article>
        <article><span>MFS transaction volume</span><strong>{format(scale.metrics.transaction_count)}<small>transactions</small></strong><p>February 2025 · web table, row 7</p><SourceLink source={sources['bb-mfs']} /></article>
        <article><span>Documented MFS cases</span><strong>{incidents.length}<small>cases in this curated set</small></strong><p>Not a national incident count</p><a href="#ev-timeline">Explore cases ↓</a></article>
        <article><span>Verified official sources</span><strong>{official.length}<small>of {verified.length} checked source records</small></strong><p>Unavailable sources excluded</p><a href="#ev-sources">Inspect source quality ↓</a></article>
      </section>

      <section className="ev-section"><div className="ev-section-head"><div><span className="ev-eyebrow">WHAT DOES THE EVIDENCE SHOW?</span><h2>Explore the evidence</h2></div><span>{filtered.length} of {manifest.items.length} evidence items</span></div>
        <div className="ev-filters"><label><span>Search evidence</span><input placeholder="Source, incident or risk…" value={query} onChange={(e) => setQuery(e.target.value)} /></label><label><span>Source quality</span><select value={tier} onChange={(e) => setTier(e.target.value)}><option value="all">All tiers</option>{Object.entries(QUALITY).map(([key, name]) => <option value={key} key={key}>Tier {key} · {name}</option>)}</select></label></div>
        <div className="ev-categories" role="group" aria-label="Evidence categories">{categories.map((c) => <button key={c} aria-pressed={category === c} className={category === c ? 'selected' : ''} onClick={() => setCategory(c)}>{c}</button>)}</div>
        <div className="ev-grid">{filtered.map((item) => <article className="ev-card" key={item.id} id={`evidence-${item.id}`}>
          <div className="ev-card-meta"><Quality source={sources[item.source_id]} /><time>{item.date}</time></div>
          <h3>{item.title}</h3><p>{item.claim}</p><span className="ev-relevance">{item.relevance}</span>
          <details><summary>What this supports—and its limits</summary><dl><dt>Supports</dt><dd>{item.supports}</dd><dt>Does not establish</dt><dd>{item.limitations}</dd><dt>Thamun response</dt><dd>{item.feature} · design relevance, not demonstrated prevention</dd><dt>Source locator</dt><dd>{sources[item.source_id].locator}</dd></dl></details>
          <SourceLink source={sources[item.source_id]} />
        </article>)}</div>
        {!filtered.length && <p className="ev-empty" role="status">No evidence matches these filters. Try another category or source tier.</p>}
      </section>

      <section className="ev-section" id="ev-analysis"><div className="ev-section-head"><div><span className="ev-eyebrow">MEASURED SCALE, NOT SCAM PREVALENCE</span><h2>Bangladesh Evidence — Statistical Analysis</h2></div></div>
        <div className="ev-analysis-grid"><article className="ev-card"><h3>MFS transaction value: two monthly observations</h3><p>Zero-based comparison · crore BDT</p><div className="ev-bars">{scale.comparison.map((row) => <div key={row.month}><span>{row.month}</span><div className="ev-bar-track"><i style={{ width: `${row.value_crore_bdt / 180000 * 100}%` }} /></div><strong>{format(row.value_crore_bdt)}</strong></div>)}</div><div className="ev-axis"><span>0</span><span>180,000 crore BDT</span></div><p className="ev-caption">January → February: {diff.toFixed(2)}%. Formula: (February − January) / January × 100. Monthly totals reflect different month lengths; this is not an annual trend or fraud estimate.</p><SourceLink source={sources['bb-mfs']} /><small>Metric: total monthly transaction value · period: Jan–Feb 2025 · rows 7–8 · checked {manifest.reviewed_at}</small></article>
        <article className="ev-card"><h3>Source quality in this collection</h3><div className="ev-source-counts">{Object.entries(QUALITY).map(([key, name]) => <div key={key}><span>{name}</span><strong>{verified.filter((s) => s.tier === Number(key)).length}</strong></div>)}</div><p className="ev-caption">Counts are computed from verified source records in this manifest. They measure the collection, not fraud frequency or independent corroborations. Institutional hosted media and syndicated reporting are identified.</p><p className="ev-caption">No national APP rate, case-loss total, or growth series is inferred from these cases.</p></article></div>
      </section>

      <section className="ev-section" id="ev-timeline"><span className="ev-eyebrow">CASE STUDIES · NOT POPULATION STATISTICS</span><h2>Documented incident timeline</h2><div className="ev-timeline">{incidents.map((item) => <article key={item.id} className="ev-incident"><time>{item.date}<small>Article publication date</small></time><details><summary><h3>{item.title}</h3><span>{item.relevance}</span></summary><p>{item.claim}</p><dl><dt>Service</dt><dd>{item.service}</dd><dt>Amount</dt><dd>{item.amount_bdt ? `BDT ${format(item.amount_bdt)} · ${item.amount_meaning}` : 'Not verified; no amount displayed'}</dd><dt>Reported outcome</dt><dd>{item.outcome}</dd><dt>Classification limit</dt><dd>{item.limitations}</dd></dl><SourceLink source={sources[item.source_id]} /></details></article>)}</div></section>

      <section className="ev-section ev-mapping"><span className="ev-eyebrow">WHY DOES THAMUN MATTER?</span><h2>What This Means for Thamun</h2><p>Evidence motivates these prototype capabilities. It does not validate their real-world effectiveness.</p><div className="ev-map-grid">{manifest.items.filter((i) => i.id !== 'scale').map((item) => <article key={item.id}><span>{item.title}</span><b aria-hidden="true">↓</b><strong>{item.feature}</strong><a href={`#evidence-${item.id}`} onClick={() => { setCategory('All'); setTier('all'); setQuery('') }}>Inspect supporting evidence</a></article>)}</div><div className="ev-flow"><strong>Manipulation</strong><span>→</span><strong>Payment attempt</strong><span>→</span><strong>Risk + purpose check</strong><span>→</span><strong>Pause before authorization</strong><span>→</span><strong>User decides</strong></div><small>Prototype payment flow. No live wallet interception or production prevention claim.</small></section>

      <section className="ev-section" id="ev-sources"><div className="ev-section-head"><div><span className="ev-eyebrow">WHERE DID THIS COME FROM?</span><h2>Source explorer</h2></div><button className="btn" onClick={openReport}>{showReport ? 'Hide full report' : 'View Full Bangladesh Evidence Report'}</button></div>
        <p className="ev-caption">Tier 1 = official. Tier 2 = institutional/research. Tier 3 = established media. Tier describes provenance, not certainty. A verified page does not independently verify every allegation it reports.</p>
        <div className="ev-grid">{manifest.sources.map((source) => <article className={`ev-card ${source.status !== 'verified' ? 'ev-unverified' : ''}`} key={source.id}><Quality source={source} /><h3>{source.organization}</h3><p>{source.title}</p><span className={`ev-status ${source.status}`}>{source.status === 'verified' ? 'Source text checked' : source.status === 'not_used' ? 'Not used' : 'Not verified from available source'}</span><small>Published: {source.date || 'Not supplied'} · checked: {source.checked_at}{source.period ? ` · reporting month: ${source.period}` : ''}</small>{source.locator && <small>{source.locator}</small>}{source.note && <p className="ev-caption">{source.note}</p>}<SourceLink source={source} />{source.retrieval_url && <a href={source.retrieval_url} target="_blank" rel="noopener noreferrer">Checked publisher mirror ↗</a>}<div className="ev-extracted">{manifest.items.filter((i) => i.source_id === source.id).map((i) => <a key={i.id} href={`#evidence-${i.id}`} onClick={() => { setCategory('All'); setTier('all'); setQuery('') }}>{i.title} ↑</a>)}</div></article>)}</div>
        {showReport && <article className="ev-report"><h3>Full evidence report</h3><a className="btn" href="/evidence/report.pdf" target="_blank" rel="noopener noreferrer">Open PDF report ↗</a>{reportError ? <p role="alert">{reportError}</p> : report ? <pre>{report}</pre> : <p role="status">Loading report…</p>}</article>}
      </section>
      <footer className="ev-footer"><strong>Pause. Understand. Decide.</strong><span>Public evidence ≠ model validation. Synthetic evaluation ≠ production performance.</span><button className="btn primary" onClick={onBack}>Return to payment demo</button></footer>
    </div>
  </main>
}
