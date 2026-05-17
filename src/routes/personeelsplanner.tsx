import { createFileRoute } from "@tanstack/react-router";
import { PageStub } from "@/components/dashboard/Page";

export const Route = createFileRoute("/personeelsplanner")({ component: () => <PageStub title="Personeelsplanner" description="Wekelijks grid: koppel medewerkers aan inpakdagen." /> });
