// Plain JavaScript for the student workshop.
const clock = document.getElementById('clock');
const note = document.getElementById('clock-note');
const status = document.getElementById('status');
const startButton = document.getElementById('start-button');
const standingsBody = document.getElementById('standings-rows');
const submissionsBody = document.getElementById('submission-rows');
let snapshot = null;
let serverOffsetMs = 0;

function addCell(row, text, className = '') {
  const cell = document.createElement('td');
  cell.textContent = String(text);
  if (className) cell.className = className;
  row.appendChild(cell);
  return cell;
}

function drawStandings(data) {
  standingsBody.replaceChildren();
  data.standings.forEach(team => {
    const tr = document.createElement('tr');
    if (team.rank === 1 && team.solved > 0) tr.className = 'leader';
    addCell(tr, team.rank, 'monospace');
    addCell(tr, team.team_name);
    addCell(tr, team.solved, 'monospace');
    addCell(tr, team.penalty, 'monospace');
    data.problems.forEach(problem => {
      const result = team.problems[problem.id];
      const label = result.solved ? `+${result.wrong_before_solve || ''}` :
        result.wrong_before_solve ? `-${result.wrong_before_solve}` : '·';
      addCell(tr, label, `problem-result ${result.solved ? 'solved' : 'pending'}`);
    });
    standingsBody.appendChild(tr);
  });
}

function drawSubmissions(data) {
  submissionsBody.replaceChildren();
  document.getElementById('submission-count').textContent = `${data.submissions.length} results`;
  document.getElementById('feed-note').textContent = data.status === 'ready' ?
    'Sample data preview · starts revealing with the clock' : 'Results revealed up to the contest clock';
  data.submissions.forEach(item => {
    const tr = document.createElement('tr');
    addCell(tr, `${item.minute}m`, 'monospace');
    addCell(tr, item.team_name);
    addCell(tr, item.problem_id);
    const td = addCell(tr, item.verdict);
    td.className = `verdict ${item.verdict === 'Accepted' ? 'accepted' : 'rejected'}`;
    submissionsBody.appendChild(tr);
  });
  if (!data.submissions.length) {
    const tr = document.createElement('tr');
    const td = addCell(tr, 'No submissions yet', 'empty-row');
    td.colSpan = 4;
    submissionsBody.appendChild(tr);
  }
}

function updateClock() {
  if (!snapshot) return;
  let remaining = snapshot.duration_seconds;
  if (snapshot.started_at) {
    const serverNowMs = Date.now() + serverOffsetMs;
    const elapsed = Math.max(0, (serverNowMs - Date.parse(snapshot.started_at)) / 1000);
    remaining = Math.max(0, Math.ceil(snapshot.duration_seconds - elapsed));
  }
  const hours = Math.floor(remaining / 3600).toString().padStart(2, '0');
  const minutes = Math.floor((remaining % 3600) / 60).toString().padStart(2, '0');
  const seconds = (remaining % 60).toString().padStart(2, '0');
  clock.textContent = `${hours}:${minutes}:${seconds}`;
  const finished = snapshot.started_at && remaining === 0;
  status.textContent = !snapshot.started_at ? 'Not started' : finished ? 'Contest finished' : 'In progress';
  note.textContent = !snapshot.started_at ? 'Ready to start · 2 hours' : finished ?
    'Time is up · Final standings' : 'Shared clock · survives page refresh';
  startButton.disabled = Boolean(snapshot.started_at);
  startButton.textContent = snapshot.started_at ? 'Started' : 'Start contest';
}

async function refreshContest() {
  try {
    const response = await fetch('/api/contest', { cache: 'no-store' });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const data = await response.json();
    serverOffsetMs = Date.parse(data.server_now) - Date.now();
    snapshot = data;
    drawStandings(data);
    drawSubmissions(data);
    updateClock();
  } catch (error) {
    status.textContent = 'Connection lost · retrying';
    console.error('Could not fetch contest:', error);
  }
}

startButton.addEventListener('click', async () => {
  startButton.disabled = true;
  try {
    const response = await fetch('/api/start', { method: 'POST' });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    await refreshContest();
  } catch (error) {
    status.textContent = 'Could not start contest';
    startButton.disabled = false;
    console.error(error);
  }
});
refreshContest();
setInterval(updateClock, 1000);
setInterval(refreshContest, 2000);
