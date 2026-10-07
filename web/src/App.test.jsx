import React from 'react'
import { act, cleanup, render, screen } from '@testing-library/react'
import { afterEach, expect, it, vi } from 'vitest'
import App from './App'

vi.mock('./api', () => ({ api: { base: 'offline', customers: () => new Promise(() => {}) } }))
afterEach(() => { cleanup(); window.location.hash = ''; vi.restoreAllMocks() })

it('keeps evidence visible when source and case anchors change the hash, even with an offline backend', async () => {
  window.scrollTo = vi.fn()
  window.location.hash = '#evidence'
  render(<App />)
  expect(screen.getByRole('heading', { name: 'Bangladesh MFS Fraud & APP Evidence' })).toBeTruthy()
  await act(async () => { window.location.hash = '#ev-sources'; window.dispatchEvent(new HashChangeEvent('hashchange')) })
  expect(screen.getByRole('heading', { name: 'Bangladesh MFS Fraud & APP Evidence' })).toBeTruthy()
  await act(async () => { window.location.hash = '#evidence-dighi'; window.dispatchEvent(new HashChangeEvent('hashchange')) })
  expect(screen.getByRole('heading', { name: 'Bangladesh MFS Fraud & APP Evidence' })).toBeTruthy()
})
