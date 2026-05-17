import { createFileRoute } from "@tanstack/react-router";
import { PageStub } from "@/components/dashboard/Page";

export const Route = createFileRoute("/paklijsten")({ component: () => <PageStub title="Paklijsten" description="Afdrukbare paklijsten per boeking of per dag, inclusief klantgegevens en handtekeningveld." /> });
