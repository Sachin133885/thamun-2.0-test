import React from 'react'
import { afterEach, describe, expect, it, vi } from 'vitest'
import { cleanup, fireEvent, render, screen, within } from '@testing-library/react'
import Evidence from './Evidence'

afterEach(() => { cleanup(); vi.unstubAllGlobals() })

describe('Bangladesh evidence dashboard', () => {
  it('separates verified public evidence from synthetic evaluation and does not pretend unavailable PDF facts exist', () => {
    render(<Evidence onBack={() => {}} onLanguage={() => {}} />)
    expect(screen.getByRole('heading', { name: 'Bangladesh MFS Fraud & APP Evidence' })).toBeTruthy()
    expect(screen.getByText(/does not establish real-world MFS performance/)).toBeTruthy()
    expect(screen.getAllByText('Not verified from available source').length).toBe(3)
    expect(screen.queryByText(/p\. XX/)).toBeNull()
  })

  it('filters incident cases and shows a useful empty result for an unmatched search', () => {
    const { container } = render(<Evidence onBack={() => {}} onLanguage={() => {}} />)
    fireEvent.click(screen.getByRole('button', { name: 'Incident Case Studies', exact: true }))
    expect(container.querySelectorAll('.ev-grid')[0].querySelectorAll('.ev-card').length).toBe(2)
    fireEvent.change(screen.getByPlaceholderText('Source, incident or risk…'), { target: { value: 'no-such-case-xyz' } })
    expect(screen.getByRole('status').textContent).toContain('No evidence matches')
    fireEvent.change(screen.getByPlaceholderText('Source, incident or risk…'), { target: { value: '' } })
    fireEvent.click(screen.getByRole('button', { name: 'All', exact: true }))
    fireEvent.change(screen.getByLabelText('Source quality'), { target: { value: '1' } })
    expect(container.querySelectorAll('.ev-grid')[0].querySelectorAll('.ev-card').length).toBe(1)
  })

  it('opens an integrated report safely as text, retaining original-source links', async () => {
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue({ ok: true, text: async () => '# Full report\n<script>untrusted()</script>' }))
    const { container } = render(<Evidence onBack={() => {}} onLanguage={() => {}} />)
    fireEvent.click(screen.getByRole('button', { name: 'View Full Bangladesh Evidence Report' }))
    expect(await screen.findByText(/# Full report/)).toBeTruthy()
    expect(container.querySelector('.ev-report script')).toBeNull()
    const sourceLinks = [...container.querySelectorAll('a[target="_blank"]')]
    expect(sourceLinks.every((a) => a.rel.includes('noopener'))).toBe(true)
  })

  it('supports a Bangla title and a working return control', () => {
    const back = vi.fn()
    render(<Evidence lang="bn" onBack={back} onLanguage={() => {}} />)
    expect(screen.getByRole('heading', { name: 'বাংলাদেশের এমএফএস জালিয়াতি ও APP সম্পর্কিত প্রমাণ' })).toBeTruthy()
    fireEvent.click(screen.getByRole('button', { name: 'Return to payment demo' }))
    expect(back).toHaveBeenCalledOnce()
  })
})
