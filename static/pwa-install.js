let deferredPrompt;
let installButton;

if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/sw.js', { scope: '/' })
      .then((registration) => {
        console.log('ServiceWorker registered:', registration.scope);
        
        registration.addEventListener('updatefound', () => {
          const newWorker = registration.installing;
          newWorker.addEventListener('statechange', () => {
            if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
              showUpdateNotification();
            }
          });
        });
      })
      .catch((error) => {
        console.log('ServiceWorker registration failed:', error);
      });
  });
}

window.addEventListener('beforeinstallprompt', (e) => {
  e.preventDefault();
  deferredPrompt = e;
  showInstallPromotion();
});

function showInstallPromotion() {
  const banner = document.createElement('div');
  banner.className = 'install-banner';
  banner.id = 'install-banner';
  banner.innerHTML = `
    <div style="max-width: 800px; margin: 0 auto;">
      <p style="margin: 5px 0; font-size: 16px;">
        📱 Install Fertique AI untuk akses lebih cepat!
      </p>
      <button class="install-btn" id="install-btn">Install Aplikasi</button>
      <button class="install-btn" style="background: transparent; color: white; border: 1px solid white;" id="dismiss-btn">
        Nanti Saja
      </button>
    </div>
  `;
  
  document.body.appendChild(banner);
  
  document.getElementById('install-btn').addEventListener('click', installApp);
  document.getElementById('dismiss-btn').addEventListener('click', () => {
    banner.style.display = 'none';
    localStorage.setItem('installPromptDismissed', Date.now());
  });
  
  const dismissed = localStorage.getItem('installPromptDismissed');
  if (dismissed && (Date.now() - parseInt(dismissed)) < 7 * 24 * 60 * 60 * 1000) {
    banner.style.display = 'none';
  }
}

async function installApp() {
  if (!deferredPrompt) {
    return;
  }
  
  deferredPrompt.prompt();
  
  const { outcome } = await deferredPrompt.userChoice;
  console.log(`User response to install prompt: ${outcome}`);
  
  if (outcome === 'accepted') {
    console.log('User accepted the install prompt');
    const banner = document.getElementById('install-banner');
    if (banner) {
      banner.style.display = 'none';
    }
  }
  
  deferredPrompt = null;
}

window.addEventListener('appinstalled', () => {
  console.log('Fertique AI has been installed');
  const banner = document.getElementById('install-banner');
  if (banner) {
    banner.style.display = 'none';
  }
  
  if ('analytics' in window) {
    analytics.logEvent('app_installed');
  }
});

function showUpdateNotification() {
  const notification = document.createElement('div');
  notification.style.cssText = `
    position: fixed;
    top: 20px;
    right: 20px;
    background: #2E7D32;
    color: white;
    padding: 15px 20px;
    border-radius: 10px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    z-index: 10000;
    max-width: 300px;
  `;
  notification.innerHTML = `
    <p style="margin: 0 0 10px 0;"><strong>Update Tersedia!</strong></p>
    <button onclick="location.reload()" style="
      background: white;
      color: #2E7D32;
      border: none;
      padding: 8px 16px;
      border-radius: 5px;
      cursor: pointer;
      font-weight: bold;
    ">Refresh Sekarang</button>
  `;
  document.body.appendChild(notification);
  
  setTimeout(() => {
    if (notification.parentNode) {
      notification.remove();
    }
  }, 10000);
}

if (window.matchMedia('(display-mode: standalone)').matches || window.navigator.standalone === true) {
  console.log('Running in standalone mode (installed as app)');
  document.documentElement.classList.add('standalone-mode');
}

if ('Notification' in window && Notification.permission === 'default') {
  setTimeout(() => {
    Notification.requestPermission().then((permission) => {
      console.log('Notification permission:', permission);
    });
  }, 5000);
}
