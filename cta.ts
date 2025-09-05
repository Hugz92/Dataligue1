// netlify/edge-functions/cta.ts
// Logs click_cta to GA4 server-side (no UI step), sets cookies (cid + utm_*), then redirects to Brevo.
//
// Required: create a GA4 Measurement Protocol API secret
// GA4 → Admin → Data streams → choose your Web stream → Measurement Protocol API secrets → Create
// Put it in GA_API_SECRET below.

const GA_MEASUREMENT_ID = "G-7EXC0P38K5"; // your GA4 ID
const GA_API_SECRET = "6eAtVWmxTGi10yc7LmD0fg"; // <-- fill this
const BREVO_TARGET = "https://9993d118.sibforms.com/serve/MUIFAIfr1XLjDYI4YSAAC6eff0C_gyvartLAUHoXik0N54Oyje40Bz3TPUAhN-dcdb6eSAyZPrgHsHFREjcmA1jDhoQhzMn_fIGB_re1XM0gTaSV6IXZKoPoOt2SmphEc_KflKS1p0JVge0DUqoBmRMOjwp_fP2TqjQg_LBtnWkN0fgfmpvAq8ukpRNq-qjRJMtC4Tjlnv3yEZ53"; // your Brevo form URL (long)

function parseCookies(header: string | null): Record<string,string> {
  const out: Record<string,string> = {}
  if (!header) return out;
  const parts = header.split(/;\s*/);
  for (const p of parts) {
    const i = p.indexOf("=");
    if (i > -1) out[decodeURIComponent(p.slice(0,i))] = decodeURIComponent(p.slice(i+1));
  }
  return out;
}

function cookie(name: string, value: string, maxAge=60*60*24*180) {
  return `${name}=${value}; Path=/; Max-Age=${maxAge}; SameSite=Lax; Secure`;
}

function mapSource(pathname: string) {
  // /ig/<content?>, /x/<content?>, /fb/<content?>
  const [, first, ...rest] = pathname.split("/"); // ["", "ig", "reel"]
  const content = rest.join("/") || "bio";
  switch (first) {
    case "ig": return { source: "instagram", medium: "social", content };
    case "x":  return { source: "twitter",   medium: "social", content };
    case "fb": return { source: "facebook",  medium: "social", content };
    default:   return { source: "site",      medium: "referral", content };
  }
}

export default async (request: Request) => {
  const url = new URL(request.url);
  const { source, medium, content } = mapSource(url.pathname);
  const cookies = parseCookies(request.headers.get("cookie"));
  let cid = cookies["cid"];
  if (!cid) cid = crypto.randomUUID();

  // Build redirect target (append UTM)
  const target = new URL(BREVO_TARGET);
  target.searchParams.set("utm_source", source);
  target.searchParams.set("utm_medium", medium);
  target.searchParams.set("utm_campaign", "signup_l1_2025");
  target.searchParams.set("utm_content", content);

  // Fire GA4 Measurement Protocol event (server-side)
  // Doc: https://developers.google.com/analytics/devguides/collection/protocol/ga4/reference
  const body = {
    client_id: cid,
    non_personalized_ads: true,
    events: [{
      name: "click_cta",
      params: {
        form_name: "Brevo - Inscription newsletter",
        origin: source,
        medium: medium,
        variant: content,
        page_location: request.url,
      }
    }]
  };

  try {
    await fetch(`https://www.google-analytics.com/mp/collect?measurement_id=${GA_MEASUREMENT_ID}&api_secret=${GA_API_SECRET}`, {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify(body)
    });
  } catch (_) { /* ignore network errors, still redirect */ }

  // Set cookies (cid + utm_*) so the thank-you page can reuse them
  const headers = new Headers();
  headers.append("Set-Cookie", cookie("cid", cid));
  headers.append("Set-Cookie", cookie("utm_source", source));
  headers.append("Set-Cookie", cookie("utm_medium", medium));
  headers.append("Set-Cookie", cookie("utm_campaign", "signup_l1_2025"));
  headers.append("Set-Cookie", cookie("utm_content", content));

  headers.set("Location", target.toString());
  return new Response(null, { status: 302, headers });
};
