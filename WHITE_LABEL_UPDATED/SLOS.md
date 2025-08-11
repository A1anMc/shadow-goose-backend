# 📏 Service Level Objectives (SLOs)

Availability
- API: 99.9% monthly
- Frontend: 99.9% monthly

Latency (p95)
- API: < 300 ms
- Web page TTFB: < 500 ms

Error rate
- API 5xx: < 0.5% per day

Recovery
- RTO (Recovery Time Objective): < 1 hour for SEV1
- RPO (Recovery Point Objective): < 1 hour

Alert thresholds
- Breach when SLO trends below targets for 15 min
- Page on SEV1; ticket on SEV2; log on SEV3
