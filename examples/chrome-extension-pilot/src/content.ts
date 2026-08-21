const ROOT_ID = "focus-lens-pilot";
const ACTIVE_CLASS = "focus-lens-active";
export function toggleFocus(root: ParentNode = document) {
  const items = Array.from(
    root.querySelectorAll<HTMLElement>("[data-focus-item]"),
  );
  const activate = !items.every((item) =>
    item.classList.contains(ACTIVE_CLASS),
  );
  for (const item of items) item.classList.toggle(ACTIVE_CLASS, activate);
  return { active: activate, count: items.length };
}
export function mount(root: Document = document) {
  if (root.getElementById(ROOT_ID)) return;
  const style = root.createElement("style");
  style.textContent = `#${ROOT_ID}{all:initial;position:fixed;right:20px;bottom:20px;z-index:2147483647;font-family:ui-sans-serif,system-ui,sans-serif}#${ROOT_ID} button{border:0;border-radius:999px;padding:12px 16px;background:#173c34;color:#fff;font:700 14px ui-sans-serif,system-ui,sans-serif;box-shadow:0 8px 28px #0003;cursor:pointer}#${ROOT_ID} button:focus-visible{outline:3px solid #f09b65;outline-offset:3px}.focus-lens-active{outline:3px solid #e26c45!important;outline-offset:4px!important;background:#fff4d6!important}@media(prefers-reduced-motion:no-preference){#${ROOT_ID} button{transition:transform .18s ease}#${ROOT_ID} button:hover{transform:translateY(-2px)}}`;
  root.head.append(style);
  const host = root.createElement("div");
  host.id = ROOT_ID;
  const button = root.createElement("button");
  button.type = "button";
  button.textContent = "Destacar 0 itens";
  button.setAttribute("aria-pressed", "false");
  button.addEventListener("click", () => {
    const result = toggleFocus(root);
    button.setAttribute("aria-pressed", String(result.active));
    button.textContent = result.active
      ? `Remover destaque (${result.count})`
      : `Destacar ${result.count} itens`;
  });
  host.append(button);
  root.body.append(host);
  button.textContent = `Destacar ${root.querySelectorAll("[data-focus-item]").length} itens`;
}
if (document.readyState === "loading")
  document.addEventListener("DOMContentLoaded", () => mount(), { once: true });
else mount();
