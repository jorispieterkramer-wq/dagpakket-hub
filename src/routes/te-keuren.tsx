import { createFileRoute } from "@tanstack/react-router";
import { PageStub } from "@/components/dashboard/Page";

export const Route = createFileRoute("/te-keuren")({ component: () => <PageStub title="Te keuren" description="Gefilterde lijst van items die binnen 60 dagen gekeurd moeten worden." /> });
