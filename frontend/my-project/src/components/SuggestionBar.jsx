export default function SuggestionBar() {
  const items = [
    "Analyze my coding vs meetings balance",
    "Create a goal to read 50 pages daily",
    "Summarize my week's productivity",
    "Suggest a workout routine",
  ];

  return (
    <div className="flex gap-3 overflow-x-auto pb-2">
      {items.map((i, idx) => (
        <button
          key={idx}
          className="whitespace-nowrap px-4 py-2 bg-white border rounded-xl shadow-sm text-sm hover:bg-slate-50"
        >
          {i}
        </button>
      ))}
    </div>
  );
}
