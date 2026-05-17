import { createFileRoute } from "@tanstack/react-router";
import { PageStub } from "@/components/dashboard/Page";

export const Route = createFileRoute("/keuringen")({ component: () => <PageStub title="Keuringen" description="Keuringskalender per product met automatische datumberekening." /> });
