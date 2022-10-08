import React from 'react';
import "./piku-app.css";
import { Link } from "@reach/router";


export interface PikuAppProps {
  appId: string,
  active: boolean,
  sha: string,
  self: boolean,
}

export const PikuApp = ({ appId, active, sha, self }: PikuAppProps) => {

  // TODO: Needs to do some of that sweet URL LINK STUFF
  return (
    <aside className="piku-app">
      <h2>{appId} <sup className={`applabel-${active ? 'active' : 'inactive'}`}>
        {active ? 'Active' : 'Inactive'}</sup>
      </h2>
      <ul className="app-meta">
        <li>{sha}</li>
      </ul>
      <ul>
        <li>
          <Link to={`apps/${appId}/logs`} >📖 View Logs</Link>
        </li>
        <li>
          <Link to={`apps/${appId}/config`} >🛠 Manage Config</Link>
        </li>
      </ul>

      <form className="app-action" method="POST" onSubmit={() => alert("url_for('restart_app', appid=app.id)")}>
        <button disabled={!active} type="submit">🔄 Restart</button>
      </form>
      {!self && active &&
        <form className="app-action" method="POST" onSubmit={() => alert("url_for('stop_app', appid=app.id)")}>
          <button type="submit">✋ Stop</button>
        </form>}
      {!self && !active &&
        <form className="app-action" method="POST" onSubmit={() => alert("url_for('deploy_app', appid=app.id)")}>
          <button type="submit">🏁 Start</button>
        </form>
      }
      {!self &&
        <form className="app-action" method="POST"
              onSubmit={() => window.confirm(`Are you sure you want to destroy ${appId}? This CANNOT be undone.`) ? alert("url_for('destroy_app', appid=app.id)") : null}>
          <button type="submit">☠️ Destroy</button>
        </form>
      }
    </aside>
  )
}
