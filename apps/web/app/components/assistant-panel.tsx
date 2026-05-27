export function AssistantPanel({ context, prompt }: { context: string; prompt: string }) {
  return (
    <aside className="assistant">
      <p className="eyebrow">{context}</p>
      <h2>Assistent</h2>
      <p>{prompt}</p>
      <div className="assistantInput">
        <input aria-label="Spor assistenten" placeholder="Spor assistenten" />
        <button>Vis meg</button>
      </div>
    </aside>
  );
}
