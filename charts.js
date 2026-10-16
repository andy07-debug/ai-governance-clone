// Live charts for the replica. Configs are the AI Governance app's own Chart.js 4.5.1 options (read from the
// live chart instances); data is the values shown at capture time, recovered by fitting re-renders to the
// captured bitmaps (qa/fit_charts.py) — 10/09–10/14 costs are the exact values from the live dataset.
(function () {
  var usd0 = new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: 0 });

  function costTrend() {
    return {
      type: 'line',
      data: {
        labels: ['10/09', '10/10', '10/11', '10/12', '10/13', '10/14', '10/15'],
        datasets: [{
          data: [530.0280780000003, 45.579979, 19.359871999999996, 604.7357749999993, 549.7861160000002, 541.9825619999998, 174.25],
          borderColor: '#7549F2', backgroundColor: 'rgba(117, 73, 242, 0.12)',
          pointBackgroundColor: '#5928ED', pointBorderColor: '#ffffff', pointBorderWidth: 2,
          pointRadius: 4, pointHoverRadius: 6, borderWidth: 3, fill: true, tension: 0.35
        }]
      },
      options: {
        responsive: true, maintainAspectRatio: false,
        interaction: { intersect: false, mode: 'index' },
        plugins: {
          legend: { display: false },
          tooltip: { callbacks: { label: function (c) { return 'Cost: ' + usd0.format(Number(c.raw || 0)); } } }
        },
        scales: {
          x: { title: { display: true, text: 'Date', color: '#64748b', font: { weight: 'bold' } }, grid: { display: false }, ticks: { color: '#64748b' } },
          y: {
            beginAtZero: true,
            title: { display: true, text: 'Cost (USD)', color: '#64748b', font: { weight: 'bold' } },
            grid: { color: '#e2e8f0' },
            ticks: { color: '#64748b', callback: function (v) { return usd0.format(Number(v)); } }
          }
        }
      }
    };
  }

  function requestsOverTime(values) {
    return function () {
      return {
        type: 'bar',
        data: {
          labels: ['11:11', '11:12', '11:13', '11:14', '11:15', '11:16'],
          datasets: [{
            label: 'Total Requests', data: values.slice(),
            backgroundColor: values.map(function () { return 'rgba(99, 102, 241, 0.6)'; }),
            borderColor: values.map(function () { return 'rgb(99, 102, 241)'; }),
            borderWidth: 1
          }]
        },
        options: {
          maintainAspectRatio: false,
          plugins: { legend: { display: false } },
          scales: {
            x: { ticks: { color: '#666', maxRotation: 45, autoSkip: true, maxTicksLimit: 16 }, grid: { color: '#eee' }, title: { display: true, text: 'Time', color: '#999', font: { size: 11 } } },
            y: { beginAtZero: true, ticks: { color: '#666' }, grid: { color: '#eee' }, title: { display: true, text: 'Requests', color: '#999', font: { size: 11 } } }
          }
        }
      };
    };
  }

  window.CLONE_CHARTS = {
    'llm-cost-trend': costTrend,
    'requests-05b': requestsOverTime([134, 170, 192, 201, 177, 52]),
    'requests-05d': requestsOverTime([23, 170, 192, 201, 177, 165])
  };

  var live = [];
  window.initCharts = function (root) {
    if (!window.Chart) return;
    (root || document).querySelectorAll('canvas[data-chart]').forEach(function (cv) {
      var make = window.CLONE_CHARTS[cv.getAttribute('data-chart')];
      if (make && !cv.__chart) { cv.__chart = new window.Chart(cv, make()); live.push(cv.__chart); }
    });
  };
  window.destroyCharts = function () {
    live.forEach(function (c) { c.destroy(); });
    live = [];
  };
})();
