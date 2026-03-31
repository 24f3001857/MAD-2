<script setup>
import { ref, onMounted, computed } from 'vue';
import AdminNavBar from '@/components/AdminNavBar.vue';
import api from '@/services/api';
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
  ArcElement,
  PointElement,
  LineElement,
  Filler
} from 'chart.js';
import { Doughnut, Bar } from 'vue-chartjs';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend, ArcElement, PointElement, LineElement, Filler);

const stats = ref({ student_count: 0, company_count: 0, placement_drive_count: 0 });
const loaded = ref(false);

const loadStats = async () => {
  try {
    const res = await api.get('/admin/stats');
    stats.value = res.data;
    loaded.value = true;
  } catch {
    console.error('[ERROR] Failed to load platform stats.');
  }
};

onMounted(async () => {
  await loadStats();
});

// Chart Configurations
const userChartData = computed(() => ({
  labels: ['Students', 'Companies','Placement Drives'],
  datasets: [
    {
      backgroundColor: ['#2d8cf0', '#ff4757','#00b894'],
      data: [stats.value.student_count, stats.value.company_count,stats.value.placement_drive_count],
      borderWidth: 2,
      borderColor: '#111111'
    }
  ]
}));

const userChartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'bottom',
      labels: { font: { family: "'Segoe UI', sans-serif", weight: 'bold' }, color: '#111111' }
    }
  }
};

const sourceChartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
        legend: { display: false }
    },
    scales: {
        y: { beginAtZero: true, grid: { color: 'rgba(17, 17, 17, 0.1)' } },
        x: { grid: { display: false } }
    }
};
</script>

<template>
  <div class="page">
    <AdminNavBar />

    <main class="main">
      <h3 class="section-title">▤ PLATFORM ANALYTICS DASHBOARD</h3>

      <!-- Top Overview Metrics -->
      <div class="metrics-grid">
        <div class="box metric-box bg-blue">
            <span class="metric-title">TOTAL STUDENTS</span>
            <span class="metric-value">{{ (stats.student_count).toLocaleString() }}</span>
        </div>
        <div class="box metric-box bg-green">
            <span class="metric-title">TOTAL COMPANIES</span>
            <span class="metric-value">{{ (stats.company_count).toLocaleString() }}</span>
        </div>
        <div class="box metric-box bg-purple">
            <span class="metric-title">TOTAL PLACEMENT DRIVES</span>
            <span class="metric-value">{{ (stats.placement_drive_count).toLocaleString() }}</span>
        </div>
      </div>

      <!-- Main Two Column Grid -->
      <div class="grid" v-if="loaded">

        <!-- Left Col: Demographics & Roles -->
        <div class="col">
          <div class="box chart-card">
              <h4 class="chart-title">User Demographics</h4>
              <div class="chart-container" style="height: 250px;">
                  <Doughnut :data="userChartData" :options="userChartOptions" />
              </div>
          </div>

          <div class="box chart-card">
              <h4 class="chart-title">Job Role Distribution</h4>
              <div class="chart-container" style="height: 280px;">
                  <Doughnut :data="roleChartData" :options="userChartOptions" />
              </div>
          </div>
        </div>

        <!-- Right Col: API Sourcing -->
        <div class="col">
          <div class="box chart-card" style="flex: 1;">
              <h4 class="chart-title">Harvesting Source Yield</h4>
              <div class="chart-container" style="height: 100%; min-height: 400px;">
                  <Bar :data="sourceChartData" :options="sourceChartOptions" />
              </div>
          </div>
        </div>

      </div>

    </main>
  </div>
</template>

<style scoped>
.page {
   /* Red accent for admin */
}
.main { max-width: 1100px; width: 100%; margin: 0 auto; padding: 28px 28px 60px; display: flex; flex-direction: column; gap: 24px; }
/* Metrics Banner */
.metrics-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; }
.metric-box { padding: 20px; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 4px; transition: transform 0.1s; cursor: default; }
.metric-box:hover { transform: translate(-2px, -2px); box-shadow: 6px 6px 0 var(--ink); }
.metric-title { font-weight: 900; font-size: 12px; letter-spacing: 0.1em; opacity: 0.9; }
.metric-value { font-weight: 900; font-size: 32px; letter-spacing: -1px; }
.bg-blue { background: #74b9ff; color: var(--ink); }
.bg-green { background: #55efc4; color: var(--ink); }
.bg-purple { background: #a29bfe; color: var(--ink); }
/* Grid Layouts */
.grid { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }
.col  { display: flex; flex-direction: column; gap: 24px; }
/* Charts */
.chart-card { padding: 24px; display: flex; flex-direction: column; gap: 16px; background: #fafafa; }
.chart-title { font-size: 14px; font-weight: 900; text-transform: uppercase; border-bottom: 2px solid var(--ink); padding-bottom: 8px; margin: 0; }
.chart-container { position: relative; width: 100%; }
@media (max-width: 860px) {
  .grid { grid-template-columns: 1fr; }
.metrics-grid { grid-template-columns: 1fr; }
}
</style>