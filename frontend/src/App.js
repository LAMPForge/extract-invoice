import React from 'react';
import UploadInvoice from './components/UploadInvoice';

function App() {
    return (
        <div className="App">
            <nav className="navbar navbar-expand-lg">
                <div className="container-fluid">
                    <a className="navbar-brand" href="/">Invoice Processing App</a>
                </div>
            </nav>
            <main>
                <UploadInvoice/>
            </main>
        </div>
    );
}

export default App;