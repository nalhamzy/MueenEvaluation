import { Component } from '@angular/core';
import { RouterOutlet, RouterLink, RouterLinkActive } from '@angular/router';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatSidenavModule } from '@angular/material/sidenav';
import { MatListModule } from '@angular/material/list';

@Component({
  selector: 'app-root',
  imports: [
    RouterOutlet, RouterLink, RouterLinkActive,
    MatToolbarModule, MatButtonModule, MatIconModule,
    MatSidenavModule, MatListModule,
  ],
  templateUrl: './app.html',
  styleUrl: './app.scss'
})
export class App {
  navItems = [
    { path: '/articles', label: 'Articles', icon: 'article' },
    { path: '/dataset', label: 'Dataset', icon: 'dataset' },
    { path: '/scoring', label: 'Manual Score', icon: 'score' },
    { path: '/config', label: 'Config', icon: 'settings' },
    { path: '/runs', label: 'Runs', icon: 'play_circle' },
    { path: '/runs/manual', label: 'Manual Run', icon: 'edit_note' },
    { path: '/comparison', label: 'Comparison', icon: 'compare' },
    { path: '/reports', label: 'Reports', icon: 'summarize' },
  ];
}
