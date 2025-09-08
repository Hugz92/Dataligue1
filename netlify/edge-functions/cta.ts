// netlify/edge-functions/cta.ts
// 1) Log 'click_cta' dans GA4 via Measurement Protocol (server-side)
// 2) Pose des cookies (cid + utm_*)
// 3) Redirige directement vers TA page formulaire intégrée (favicon & GA OK)
//
// Rappels :
// - GA4 → Admin → Data streams → Web stream → Measurement Protocol API secrets → Create
// - GA_MEASUREMENT_ID = ID GA4 ; GA_API_SECRET = secret Measurement Protocol.

const GA_MEASUREMENT_ID = "G-7EXC0P38K5";
const GA_API_SECRET     = "6eAtVWmxTGi10yc7LmD0fg";

// 👉 Cible désormais : la page locale qui embarque le formulaire Brevo
// (Quand ton domaine custom est prêt, remplace par https://dataligue1.fr/formulaire/)
const FORM_PAGE = "https://dataligue1.fr/formulaire/";

function parseCookies(header: string | null): Record<string,string> {
  const out: Record<string,string> = {};
  if (!header) return out;
  const parts = header.split(/;\s*/);
  for (const p of parts) {
    const i = p.indexOf("=");
    if (i > -1) out[decodeURIComponent(p.slice(0,i))] = decodeURIComponent(p.slice(i+1));
  }
  return out;
}

function cookie(name: string, value: string, maxAge = 60 * 60 * 24 * 180) {
  return `${name}=${value}; Path=/; Max-Age=${maxAge}; SameSite=Lax; Secure`;
}

function mapSource(pathname: string) {
  // Routes prévues : /ig/*, /x/*, /fb/*  (et fallback)
  // /ig/reel  => source=instagram medium=social content=reel
  // /x/bio    => source=twitter   medium=social content=bio
  const [, first, ...rest] = pathname.split("/"); // ["", "ig", "reel"]
  const content = rest.join("/") || "bio";
  switch (first) {
    case "ig": return { source: "instagram", medium: "social",  content };
    case "x":  return { source: "twitter",   medium: "social",  content };
    case "fb": return { source: "facebook",  medium: "social",  content };
    default:   return { source: "site",      medium: "referral", content };
  }
}

export default async (request: Request) => {
  const url = new URL(request.url);
  const { source, medium, content } = mapSource(url.pathname);

  // cid dans cookie (sinon UUID)
  const cookies = parseCookies(request.headers.get("cookie"));
  let cid = cookies["cid"];
  if (!cid) cid = crypto.randomUUID();

  // Cible = page locale /formulaire/ avec UTM
  const target = new URL(FORM_PAGE);

  // Conserve aussi les éventuels paramètres déjà présents (sécurité)
  url.searchParams.forEach((v, k) => target.searchParams.set(k, v));

  // Fixe nos UTM (elles écrasent si déjà présentes — souhaité)
  target.searchParams.set("utm_source",   source);
  target.searchParams.set("utm_medium",   medium);
  target.searchParams.set("utm_campaign", "signup_l1_2025");
  target.searchParams.set("utm_content",  content);

  // Événement GA4 Measurement Protocol
  const mpBody = {
    client_id: cid,
    non_personalized_ads: true,
    events: [{
      name: "click_cta",
      params: {
        form_name: "Brevo - Inscription newsletter (wrapper)",
        origin: source,
        medium: medium,
        variant: content,
        page_location: request.url,
      }
    }]
  };

  try {
    await fetch(
      `https://www.google-analytics.com/mp/collect?measurement_id=${GA_MEASUREMENT_ID}&api_secret=${GA_API_SECRET}`,
      { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify(mpBody) }
    );
  } catch {
    // On ignore les erreurs réseau, la redirection doit se faire quand même
  }

  // Cookies (cid + utm_*) pour potentielle réutilisation côté merci-inscription
  const headers = new Headers();
  headers.append("Set-Cookie", cookie("cid", cid));
  headers.append("Set-Cookie", cookie("utm_source",   source));
  headers.append("Set-Cookie", cookie("utm_medium",   medium));
  headers.append("Set-Cookie", cookie("utm_campaign", "signup_l1_2025"));
  headers.append("Set-Cookie", cookie("utm_content",  content));

  headers.set("Location", target.toString());
  return new Response(null, { status: 302, headers });
};
