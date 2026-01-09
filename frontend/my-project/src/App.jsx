
import './App.css'

function App() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-linear-to-br from-indigo-600 to-purple-600">
      <div className="bg-white p-10 rounded-2xl shadow-xl text-center">
        <h1 className="text-3xl font-bold text-slate-800 mb-4">
          Tailwind is Working 🎉
        </h1>
        <p className="text-slate-600 mb-6">
          Your Tailwind CSS setup is successful.
        </p>
        <button className="px-6 py-3 bg-indigo-600 text-white rounded-xl hover:bg-indigo-700 transition-all">
          Test Button
        </button>
      </div>
    </div>
  );
}

export default App;

